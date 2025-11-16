from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .permissions import CustomPermission

from .models import (
    Record, Message, Note, Image,
)

class PublickAPI(APIView):
    # authentication_classes = []

    def get(self, request):
        return Response(
            data={
                'success': True,
                'data': 'publick data',
                'user_id': request.user_info['id'],
                'username': request.user_info['username'],
                'role': request.user_info['role'],
                'is_auth': request.user_info['is_auth'],
            }
        )


class SecretAPI(APIView):
    permission_classes = [CustomPermission]

    def get(self, request):
        return Response(
            data={
                'success': True,
                'data': 'secret data',
                'user_id': request.user_info['id'],
                'username': request.user_info['username'],
                'role': request.user_info['role'],
                'is_auth': request.user_info['is_auth'],
            }
        )


class RecordContent(APIView):
    # permission_classes = [CustomPermission]  # для работы без токена

    def get(self, request, record_id):
        self.test_truncate()
        self.test_set_data()

        user_id = request.user_info['id']
        user_id = 1  # для работы без токена
        record_id = record_id
        record_id = Record.objects.last()  # создаем в test_set_data

        record = self.get_record(user_id, record_id.id)
        if not record:
            return Response(
                data={'detail': 'Запись не найдена'},
                status=status.HTTP_200_OK
            )

        messages = self.get_messages_qs(record_id.id)

        messages_dict = self.get_messages_dict(messages)
        # print(*messages_dict, sep='\n')

        response = {
            'record': record,
            'messages': messages_dict
        }
        # print(*response.values(), sep='\n')

        return Response(
            data=response,
            status=status.HTTP_200_OK
        )

    def test_truncate(self):
        Record.objects.all().delete()
        Message.objects.all().delete()
        Note.objects.all().delete()
        Image.objects.all().delete()

    def test_set_data(self):
        record = Record.objects.create(user_id=1, title='record title')

        msg1 = Message.objects.create(record_id=record)
        note1 = Note.objects.create(msg_id=msg1, text='any text')

        msg2 = Message.objects.create(record_id=record)
        image2 = Image.objects.create(msg_id=msg2, url='image2_url')

        msg3 = Message.objects.create(record_id=record)
        image4 = Image.objects.create(msg_id=msg3, url='image4_url')

        image3 = Image.objects.create(msg_id=msg2, url='image3_url')

    def get_record(self, user_id: int, record_id: int):
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

    def get_messages_qs(self, record_id):
        messages = Message.objects.prefetch_related('notes', 'images')
        messages = messages.filter(record_id=record_id)
        messages = list(messages.values(
            'id',
            'notes__pk', 'notes__msg_id', 'notes__text',
            'images__pk', 'images__msg_id', 'images__url'
        ))
        # print(*messages, sep='\n')
        return messages

    def get_messages_dict(self, content_list):
        response = []
        for mes in content_list:
            if mes['notes__pk']:
                self.add_note(mes, response)
            elif mes['images__pk']:
                self.add_image(mes, response)
        return response

    def add_note(self, message: dict, response: list, add_type='note'):
        note = {
            'msg_id': message['notes__msg_id'],
            'type': add_type,
            'note_id': message['notes__pk'],
            'text': message['notes__text']
        }
        response.append(note)

    def add_image(self, message: dict, response: list, add_type='images'):
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
