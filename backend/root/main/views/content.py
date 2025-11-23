from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction

from main.permissions import CustomPermission

from main.models import (
    RecordFolder, Record, Message, Note, Image,
)


class BlankDataAPI(APIView):
    """ Представления для содания тестовых данных """

    def get(self, request):
        """ Создать тестовые данные """

        self.test_truncate()
        self.test_set_data()
        return Response(status=status.HTTP_201_CREATED)

    def test_truncate(self):
        """Очистить тестовые БД"""

        Record.objects.all().delete()
        Message.objects.all().delete()
        Note.objects.all().delete()
        Image.objects.all().delete()

    def test_set_data(self):
        """Создать тестовые данные: 1 record, 1 note, 2 imgGr"""

        folder = RecordFolder.objects.create(
            user_id=1, parent_id=None,
            title='folder'
        )
        record = Record.objects.create(
            user_id=1, folder_id=folder,
            title='record title'
        )

        msg1 = Message.objects.create(record_id=record)
        note1 = Note.objects.create(msg_id=msg1, text='any text')

        msg2 = Message.objects.create(record_id=record)
        image2 = Image.objects.create(msg_id=msg2, url='image2_url')

        msg3 = Message.objects.create(record_id=record)
        image4 = Image.objects.create(msg_id=msg3, url='image4_url')

        image3 = Image.objects.create(msg_id=msg2, url='image3_url')

        note1, image2, image4, image3


class RecordContentAPI(APIView):
    # permission_classes = [CustomPermission]  # откл для работы без токена

    def get(self, request, record_id: int):

        user_id = request.user_info['id']
        user_id = 1  # для работы без токена
        record_id = record_id
        record_id = Record.objects.last().id  # получаем id последнего (если он создан) Record

        record = self.get_record(user_id, record_id)
        if not record:
            msg = 'Errof: Запись не найдена'
            return Response(data=msg, status=status.HTTP_400_BAD_REQUEST)

        messages = self.get_messages_qs(record_id)

        messages_dict = self.get_messages_dict(messages)
        # print(*messages_dict, sep='\n')

        response = {
            'record': record,
            'messages': messages_dict
        }
        # print(*response.values(), sep='\n')

        return Response(data=response, status=status.HTTP_200_OK)

    def get_record(self, user_id: int, record_id: int):
        """Получить конкретный Record по record_id с проверкой user_id"""

        try:
            record = Record.objects.get(user_id=user_id, pk=record_id)
            record_dict = {
                'record_id': record.pk,
                'user_id': record.user_id,
                'title': record.title,
            }
            # print(record_dict)
            return record_dict
        except Record.DoesNotExist:
            return None

    def get_messages_qs(self, record_id: int):
        """Получить все messages (с контентом) по record_id"""

        messages = Message.objects.prefetch_related('notes', 'images')
        messages = messages.filter(record_id=record_id)
        messages = list(messages.values(
            'id',
            'notes__pk', 'notes__msg_id', 'notes__text',
            'images__pk', 'images__msg_id', 'images__url'
        ))
        # print(*messages, sep='\n')
        return messages

    def get_messages_dict(self, content_list: list):
        """Формируем готовые msg объекты без линих полей"""

        response = []
        for mes in content_list:
            if mes['notes__pk']:
                self.add_note(mes, response)
            elif mes['images__pk']:
                self.add_image(mes, response)
        return response

    def add_note(self, message: dict, response: list, add_type='note'):
        """Формируем Note объект для response"""

        note = {
            'msg_id': message['notes__msg_id'],
            'type': add_type,
            'note_id': message['notes__pk'],
            'text': message['notes__text']
        }
        response.append(note)

    def add_image(self, message: dict, response: list, add_type='images'):
        """Формируем Images объект для response (с объединением image в 1 блок)
        """

        if (
            len(response) == 0 or
            response[-1]['type'] != add_type or
            response[-1]['msg_id'] != message['images__msg_id']
        ):
            new_images_group = {
                'msg_id': message['images__msg_id'],
                'type': add_type,
                add_type: []
            }
            response.append(new_images_group)

        response[-1][add_type].append({
            'image_id': message['images__pk'],
            'url': message['images__url']
        })


class NoteAPI(APIView):
    """ The main Note view """

    # permission_classes = [CustomPermission]  # откл для работы без токена

    def get(self, request, record_id, note_id):
        """ Gettings the note """

        user_id = request.user_info['id']
        user_id = 1  # для работы без токена

        try:
            note = Note.objects.select_related(
                    'msg_id', 'msg_id__record_id'
                ).get(
                    pk=note_id, msg_id__record_id__user_id=user_id,
                    msg_id__record_id=record_id
                )
        except Note.DoesNotExist:
            msg = 'Error: запись не найдена'
            return Response(data=msg, status=status.HTTP_404_NOT_FOUND)

        response_note = {
            "pk": note.pk,
            "user_id": note.msg_id.record_id.user_id,
            'text': note.text,
        }
        return Response(data=response_note, status=status.HTTP_200_OK)

    def post(self, request, record_id):
        """ Creating the new note """

        user_id = request.user_info['id']
        user_id = 1  # для работы без токена

        text = request.data['text']
        record_id = request.data['record_id']

        if not text:
            msg = 'Error: отсутствует текст'
            return Response(data=msg, status=status.HTTP_400_BAD_REQUEST)

        if len(text) >= 10_000:
            msg = 'Error: текст слишком длинный'
            return Response(data=msg, status=status.HTTP_400_BAD_REQUEST)

        try:
            record = Record.objects.get(pk=record_id, user_id=user_id)
        except Record.DoesNotExist:
            msg = 'Error: заметка не найдена'
            return Response(data=msg, status=status.HTTP_404_NOT_FOUND)

        try:
            with transaction.atomic():
                message = Message.objects.create(record_id=record)
                note = Note.objects.create(msg_id=message, text=text)
        except transaction.TransactionManagementError:
            msg = 'Transaction error: запись не удалена'
            return Response(data=msg, status=status.HTTP_400_BAD_REQUEST)

        msg = f'Запись сохранена, id={note.pk}'
        return Response(data=msg, status=status.HTTP_201_CREATED)

    def patch(self, request, record_id, note_id):
        """ Update note fields """

        user_id = request.user_info['id']
        user_id = 1  # для работы без токена

        text = request.data['text']
        try:
            note = Note.objects.select_related(
                'msg_id', 'msg_id__record_id'
            ).get(pk=note_id, msg_id__record_id__user_id=user_id,
                  msg_id__record_id=record_id)
        except Note.DoesNotExist:
            msg = 'Error: запись не найдена'
            return Response(data=msg, status=status.HTTP_404_NOT_FOUND)

        if (note.text == text):
            msg = 'Текст не изменен'
            return Response(data=msg, status=status.HTTP_200_OK)

        note.text = text
        note.save()

        return Response('Новый текст сохранен', status=status.HTTP_200_OK)

    def delete(self, request, record_id, note_id):
        """ Removing the note """

        user_id = request.user_info['id']
        user_id = 1  # для работы без токена

        try:
            note = Note.objects.select_related(
                'msg_id', 'msg_id__record_id'
            ).get(pk=note_id, msg_id__record_id__user_id=user_id,
                  msg_id__record_id=record_id)
        except Note.DoesNotExist:
            msg = 'Error: запись не найдена'
            return Response(data=msg, status=status.HTTP_404_NOT_FOUND)

        try:
            with transaction.atomic():
                note.msg_id.delete()
                note.delete()
        except transaction.TransactionManagementError:
            msg = 'Transaction error: запись не удалена'
            return Response(data=msg, status=status.HTTP_400_BAD_REQUEST)

        return Response('Запись удалена', status=status.HTTP_200_OK)


class ImageAPI(APIView):
    """ The single Image view """

    # permission_classes = [CustomPermission]  # откл для работы без токена

    def get(self, request, record_id, image_id):
        """ Gettings the single image """

        user_id = request.user_info['id']
        user_id = 1  # для работы без токена

        try:
            image = Image.objects.select_related('msg_id', 'msg_id__record_id')
            image = image.get(image_id=image_id, msg_id__record_id=record_id,
                              msg_id__record_id__user_id=user_id)
        except Image.DoesNotExist:
            msg = 'Error: картинка не найдена'
            return Response(data=msg, status=status.HTTP_404_NOT_FOUND)

        return Response(image.url, status=status.HTTP_200_OK)

    def post(self, request, record_id):
        """ Add the image to the existing message """

        user_id = request.user_info['id']
        user_id = 1  # для работы без токена

        new_url = request.data['file_name']
        msg_id = request.data['message_id']
        if not (new_url and msg_id):
            msg = 'Error: данные не переданы'
            return Response(data=msg, status=status.HTTP_400_BAD_REQUEST)

        try:
            message = Message.objects.select_related('record_id').get(
                record_id=record_id, msg_id=msg_id, record_id__user_id=user_id
            )
        except Message.DoesNotExist:
            msg = 'Error: сообщение не найдено'
            return Response(data=msg, status=status.HTTP_404_NOT_FOUND)

        img = Image.objects.create(msg_id=message, url=new_url)

        msg = f'Картинка {img.pk} добавлена'
        return Response(data=msg, status=status.HTTP_201_CREATED)

    def delete(self, request, record_id, image_id):
        """ Removing the singe image from the  message """

        user_id = request.user_info['id']
        user_id = 1  # для работы без токена

        try:
            img = Image.objects.select_related(
                'msg_id', 'msg_id__record_id', 'images'
            ).get(
                pk=image_id, msg_id__record_id=record_id,
                msg_id__record_id__user_id=user_id,
            )
        except Image.DoesNotExist:
            msg = 'Error: картинка не найдена'
            return Response(data=msg, status=status.HTTP_404_NOT_FOUND)

        try:
            with transaction.atomic():
                if len(img.msg_id.images.all()) == 1:
                    img.msg_id.delete()  # img должна удалиться каскадно
                else:
                    img.delete()
        except transaction.TransactionManagementError:
            msg = 'Transaction error: картинка не удалена'
            return Response(data=msg, status=status.HTTP_400_BAD_REQUEST)

        msg = 'Картинка удалена'
        return Response(data=msg, status=status.HTTP_200_OK)


class ImagesAPI(APIView):
    """ The block Image view """

    def get(self, request, record_id, msg_id):
        """ Creating the images block """

        user_id = request.user_info['id']
        user_id = 1  # для работы без токена

        try:
            message = Message.objects.select_related('record_id', 'images').get(
                msg_id=msg_id, msg_id__record_id=record_id,
                msg_id__record_id__user_id=user_id
            )
        except Message.DoesNotExist:
            msg = 'Error: сообщение не найдено'
            return Response(data=msg, status=status.HTTP_404_NOT_FOUND)

        images = list(message.images.all().values('url'))
        # msg_id = request.data['message_id']
        return Response(data=images, status=status.HTTP_200_OK)

    def post(self, request, record_id):
        """ Creating the new images block """

        user_id = request.user_info['id']
        user_id = 1  # для работы без токена

        try:
            record = Record.objects.get(record_id=record_id, user_id=user_id)
        except Record.DoesNotExist:
            msg = 'Error: заметка не найдена'
            return Response(data=msg, status=status.HTTP_404_NOT_FOUND)

        try:
            with transaction.atomic():
                message = Message.objects.create(record_id=record)

                files = []
                for file in request.data['url']:
                    files.append(Image(msg_id=message, url=file))
                Image.objects.bulk_create(files)
        except transaction.TransactionManagementError:
            msg = 'Error: Ошибка сохранения картинок'
            return Response(data=msg, status=status.HTTP_400_BAD_REQUEST)

        msg = f'Блок картинок {message.pk} сохранены'
        return Response(data=msg, status=status.HTTP_201_CREATED)

    def delete(self, request, record_id, msg_id):
        """ Removing the images block """

        user_id = request.user_info['id']
        user_id = 1  # для работы без токена

        try:
            message = Message.objects.select_related('record_id').get(
                msg_id=msg_id, msg_id__record_id=record_id,
                msg_id__record_id__user_id=user_id
            )
        except Message.DoesNotExist:
            msg = 'Error: сообщение не найдено'
            return Response(data=msg, status=status.HTTP_404_NOT_FOUND)

        message.delete()
        msg = f'Блок картинок {message.pk} удален'
        return Response(data=msg, status=status.HTTP_200_OK)
