import os
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction
from django.conf import settings

from main.permissions import CustomPermission

from main.models import (
    Record, Message, Note, Image,
)
from main.serializers.contentSerializer import (
    NoteGetSerializer, NoteWriteSerializer,
    ImageGetSerializer, ImageCreateSerializer,
    ImagesGetSerializer, ImagesCreateSerializer
)


class BlankDataAPI(APIView):
    """ Представления для содания тестовых данных """

    def get(self, request):
        """ Создать тестовые данные """

        self.test_truncate()
        self.test_set_data(request)
        return Response(status=status.HTTP_201_CREATED)

    def test_truncate(self):
        """Очистить тестовые БД"""

        # Record.objects.all().delete()
        Message.objects.all().delete()
        Note.objects.all().delete()
        Image.objects.all().delete()

    def test_set_data(self, request):
        """Создать тестовые данные: 1 record, 1 note, 2 imgGr"""

        user_id = 1

        record = Record.objects.first()  # он уже должен лежать в root

        msg1 = Message.objects.create(record_id=record)
        note1 = Note.objects.create(msg_id=msg1, text='any text')

        msg2 = Message.objects.create(record_id=record)
        img_2_path = r"C:\Users\Engineer Paul\Desktop\Python_temp\Django\Diary2.0\test_imgs\1.jpg"
        image2 = self.create_image_from_file(msg2, img_2_path, user_id)

        msg3 = Message.objects.create(record_id=record)
        img_4_path = r"C:\Users\Engineer Paul\Desktop\Python_temp\Django\Diary2.0\test_imgs\2.jpg"
        image4 = self.create_image_from_file(msg3, img_4_path, user_id)

        img_3_path = r"C:\Users\Engineer Paul\Desktop\Python_temp\Django\Diary2.0\test_imgs\3.jpg"
        image3 = self.create_image_from_file(msg2, img_3_path, user_id)

        imgs = Image.objects.all()
        print(imgs)
        for img in imgs:
            print(img.file)
            full_url = request.build_absolute_uri(img.file.url)
            print(full_url)

    def create_image_from_file(self, msg, file_path, user_id):
        """Создать Image из файла на диске"""
        with open(file_path, 'rb') as f:
            filename = os.path.basename(file_path)
            image = Image(msg_id=msg, name=filename, user_id=user_id)
            # добавить файл можно только через save
            image.file.save(filename, f, save=True)
        return image


class RecordContentAPI(APIView):
    """Вывод всей информации (детали и контент) по всей заметке"""
    # permission_classes = [CustomPermission]  # откл для работы без токена

    def get(self, request, record_id: int):
        """Получение всего контента заметки в одном запросе.
        Инфа самой заметки - response['record'],
        Контент заметки - response['messages'].
        В контент уже вложены тексты сообщений и адресы картинок.
        response['messages'] = list(
            dict(msg_id, type,
                (note_id, text) или (list(image_id, name, url))
            )
        )"""

        user_id = request.user_info['id']
        user_id = 1  # исправить. для работы без токена

        record = self.get_record(user_id, record_id)
        if not record:
            msg = 'Error: Запись не найдена'
            return Response(data=msg, status=status.HTTP_400_BAD_REQUEST)

        messages = self.get_messages_qs(request, record_id)

        messages_dict = self.get_messages_dict(messages)

        response = {
            'record': record,
            'messages': messages_dict
        }

        return Response(data=response, status=status.HTTP_200_OK)

    def get_record(self, user_id: int, record_id: int):
        """Получить конкретный Record по record_id с проверкой user_id"""

        try:
            record = Record.objects.get(user_id=user_id, pk=record_id)
            record_dict = {
                'record_id': record.pk,
                'user_id': record.user_id,
                'title': record.title,
                'description': record.description,
                'color': record.color,
            }
            # print(record_dict)
            return record_dict
        except Record.DoesNotExist:
            return None

    def get_messages_qs(self, request, record_id: int):
        """Получить все messages (с контентом) по record_id"""

        messages = Message.objects.prefetch_related('notes', 'images')
        messages = messages.filter(record_id=record_id)
        messages = list(messages.values(
            'id',
            'notes__pk', 'notes__msg_id', 'notes__text', 'notes__created_at', 'notes__changed_at',
            'images__pk', 'images__msg_id', 'images__name', 'images__file'
        ))

        for msg in messages:
            if msg.get('images__file'):
                relative_url = f"{settings.MEDIA_URL}{msg['images__file']}"
                msg['images__url'] = request.build_absolute_uri(relative_url)
        # print(*messages, sep='\n')
        return messages

    def get_messages_dict(self, content_list: list):
        """Формируем готовые msg объекты без лишних полей"""

        messages_dict = []
        for mes in content_list:
            if mes['notes__pk']:
                self.add_note(mes, messages_dict)
            elif mes['images__pk']:
                self.add_image(mes, messages_dict)
        return messages_dict

    def add_note(self, message: dict, response: list, add_type='note'):
        """Формируем Note объект для response"""

        note = {
            'msg_id': message['notes__msg_id'],
            'type': add_type,
            'note_id': message['notes__pk'],
            'text': message['notes__text'],
            'created_at': message['notes__created_at'],
            'changed_at': message['notes__changed_at']
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
            'name': message['images__name'],
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

        return Response(NoteGetSerializer(note).data, status=status.HTTP_200_OK)

    def post(self, request, record_id):
        """ Creating the new note """

        user_id = request.user_info['id']
        user_id = 1  # для работы без токена

        serializer = NoteWriteSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        try:
            record = Record.objects.get(pk=record_id, user_id=user_id)
        except Record.DoesNotExist:
            msg = 'Error: заметка не найдена'
            return Response(data=msg, status=status.HTTP_404_NOT_FOUND)

        try:
            with transaction.atomic():
                message = Message.objects.create(record_id=record)
                note = serializer.save(msg_id=message)
        except transaction.TransactionManagementError:
            msg = 'Transaction error: запись не удалена'
            return Response(data=msg, status=status.HTTP_400_BAD_REQUEST)

        msg = f'Запись сохранена, id={note.pk}'
        return Response(data=msg, status=status.HTTP_201_CREATED)

    def patch(self, request, record_id, note_id):
        """ Update note fields """

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

        serializer = NoteWriteSerializer(note, data=request.data, partial=True)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()
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
            note.msg_id.delete()
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
            image = image.get(pk=image_id, msg_id__record_id=record_id,
                              msg_id__record_id__user_id=user_id)
        except Image.DoesNotExist:
            msg = 'Error: картинка не найдена'
            return Response(data=msg, status=status.HTTP_404_NOT_FOUND)

        serializer = ImageGetSerializer(image, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, record_id):
        """ Add the image to the existing message """

        user_id = request.user_info['id']
        user_id = 1  # для работы без токена

        msg_id = request.data.get('msg_id')
        if not msg_id:
            return Response('Error: msg_id обязателен', status=status.HTTP_400_BAD_REQUEST)

        try:
            message = Message.objects.select_related('record_id').get(
                pk=msg_id, record_id_id=record_id, record_id__user_id=user_id
            )
        except Message.DoesNotExist:
            msg = 'Error: сообщение не найдено'
            return Response(data=msg, status=status.HTTP_404_NOT_FOUND)

        serializer = ImageCreateSerializer(
            data=request.data,
            context={'user_id': user_id, 'message': message}
        )
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        img = serializer.save()

        msg = f'Картинка {img.pk} добавлена'
        return Response(data=msg, status=status.HTTP_201_CREATED)

    def delete(self, request, record_id, image_id):
        """ Removing the singe image from the  message """

        user_id = request.user_info['id']
        user_id = 1  # для работы без токена

        try:
            img = Image.objects.prefetch_related('msg_id__images').select_related(
                'msg_id', 'msg_id__record_id'
            ).get(
                pk=image_id, msg_id__record_id=record_id,
                msg_id__record_id__user_id=user_id,
            )
        except Image.DoesNotExist:
            msg = 'Error: картинка не найдена'
            return Response(data=msg, status=status.HTTP_404_NOT_FOUND)

        try:
            with transaction.atomic():
                img.file.delete(save=False)
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
            message = Message.objects.prefetch_related(
                'images'
            ).select_related('record_id').get(
                pk=msg_id, record_id_id=record_id,
                record_id__user_id=user_id
            )
        except Message.DoesNotExist:
            msg = 'Error: сообщение не найдено'
            return Response(data=msg, status=status.HTTP_404_NOT_FOUND)

        serializer = ImagesGetSerializer(
            message.images.all(), many=True, context={'request': request}
        )
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def post(self, request, record_id):
        """ Creating the new images block """

        user_id = request.user_info['id']
        user_id = 1  # для работы без токена

        try:
            record = Record.objects.get(pk=record_id, user_id=user_id)
        except Record.DoesNotExist:
            msg = 'Error: заметка не найдена'
            return Response(data=msg, status=status.HTTP_404_NOT_FOUND)

        # Получаем список файлов из FormData
        files = request.FILES.getlist('file')
        if not files:
            return Response('Error: файлы не найдены', status=status.HTTP_400_BAD_REQUEST)

        # Преобразуем список файлов в список словарей для сериализатора с many=True
        data_list = []
        for file in files:
            data_list.append({'file': file})

        try:
            with transaction.atomic():
                message = Message.objects.create(record_id=record)
                serializer = ImagesCreateSerializer(
                    data=data_list, many=True,
                    context={'user_id': user_id, 'message': message}
                )
                if not serializer.is_valid():
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                serializer.save()
        except (transaction.TransactionManagementError, ValueError) as e:
            msg = f'Error: Ошибка сохранения картинок - {e}'
            return Response(data=msg, status=status.HTTP_400_BAD_REQUEST)

        msg = f'Блок картинок {message.pk} сохранен'
        return Response(data=msg, status=status.HTTP_201_CREATED)

    def delete(self, request, record_id, msg_id):
        """ Removing the images block """

        user_id = request.user_info['id']
        user_id = 1  # для работы без токена

        try:
            message = Message.objects.prefetch_related('images').select_related('record_id').get(
                pk=msg_id, record_id_id=record_id,
                record_id__user_id=user_id
            )
        except Message.DoesNotExist:
            msg = 'Error: сообщение не найдено'
            return Response(data=msg, status=status.HTTP_404_NOT_FOUND)

        try:
            with transaction.atomic():
                for img in message.images.all():
                    img.file.delete(save=False)
                message.delete()
        except Exception:
            msg = 'Error: ошибка удаления блока картинок'
            return Response(data=msg, status=status.HTTP_400_BAD_REQUEST)

        msg = f'Блок картинок {msg_id} удален'
        return Response(data=msg, status=status.HTTP_200_OK)
