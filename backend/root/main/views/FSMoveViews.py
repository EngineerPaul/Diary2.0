from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction

from main.models import (
    RecordFolder, Record,
    # NoticeFolder, Notice
)
from main.serializers.FSMoveSerializers import (
    MoveInsideSerializer, MoveBetweenSerializer
)


class MoveBetweenAPI(APIView):
    """ API for moving an object between another objects in a folder """

    def post(self, request):

        user_id = request.user_info['id']

        serializer = MoveBetweenSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        validated_data = serializer.validated_data
        if validated_data['type'] == 'record':
            resp = self.move_record(validated_data, user_id)
        elif validated_data['type'] == 'recordFolder':
            resp = self.move_record_folder(validated_data, user_id)
        elif validated_data['type'] == 'notice':
            resp = self.move_notice(validated_data, user_id)
        elif validated_data['type'] == 'noticeFolder':
            resp = self.move_notice_folder(validated_data, user_id)
        else:
            resp = {'success': False, 'msg': 'Неверный тип данных'}

        if not resp['success']:
            return Response(resp, status=status.HTTP_400_BAD_REQUEST)

        return Response(resp, status=status.HTTP_200_OK)

    def move_record(self, data, user_id):
        """Change the record order inside the folder"""
        try:
            Record.objects.get(pk=data['object_id'], user_id=user_id)
            folder = RecordFolder.objects.get(pk=data['folder_id'], user_id=user_id)
        except (Record.DoesNotExist, RecordFolder.DoesNotExist):
            return {'success': False, 'msg': 'Данные не найдены'}

        folder.nested_objects = ','.join(map(str, data['nested_list']))
        folder.save()

        return {'success': True, 'msg': 'Данные сохранены'}

    def move_record_folder(self, data, user_id):
        """Change the record folder order inside the parent folder"""
        try:
            RecordFolder.objects.get(pk=data['object_id'], user_id=user_id)
            parent_folder = RecordFolder.objects.get(pk=data['folder_id'], user_id=user_id)
        except RecordFolder.DoesNotExist:
            return {'success': False, 'msg': 'Данные не найдены'}

        parent_folder.nested_folders = ','.join(map(str, data['nested_list']))
        parent_folder.save()

        return {'success': True, 'msg': 'Данные сохранены'}

    def move_notice(self, data, user_id):
        """Change the notice order inside the folder"""
        try:
            pass
            # Notice.objects.get(pk=data['object_id'], user_id=user_id)
            # folder = NoticeFolder.objects.get(pk=data['folder_id'], user_id=user_id)
        except Exception:  # (Notice.DoesNotExist, NoticeFolder.DoesNotExist)
            return {'success': False, 'msg': 'Данные не найдены'}

        # folder.nested_notices = ','.join(map(str, data['nested_list']))
        # folder.save()

        return {'success': True, 'msg': 'Данные сохранены'}

    def move_notice_folder(self, data, user_id):
        """Change the notice folder order inside the parent folder"""
        try:
            pass
            # NoticeFolder.objects.get(pk=data['object_id'], user_id=user_id)
            # parent_folder = NoticeFolder.objects.get(pk=data['folder_id'], user_id=user_id)
        except Exception:  # NoticeFolder.DoesNotExist
            return {'success': False, 'msg': 'Данные не найдены'}

        # parent_folder.nested_folders = ','.join(map(str, data['nested_list']))
        # parent_folder.save()

        return {'success': True, 'msg': 'Данные сохранены'}


class MoveInsideAPI(APIView):
    """ API for moving an object between folders """

    def post(self, request):

        user_id = request.user_info['id']

        serializer = MoveInsideSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        validated_data = serializer.validated_data
        if validated_data['type'] == 'record':
            resp = self.move_record(validated_data, user_id)
        elif validated_data['type'] == 'recordFolder':
            resp = self.move_record_folder(validated_data, user_id)
        elif validated_data['type'] == 'notice':
            resp = self.move_notice(validated_data, user_id)
        elif validated_data['type'] == 'noticeFolder':
            resp = self.move_notice_folder(validated_data, user_id)
        else:
            resp = {'success': False, 'msg': 'Неверный тип данных'}

        if not resp['success']:
            return Response(resp, status=status.HTTP_400_BAD_REQUEST)

        return Response(resp, status=status.HTTP_200_OK)

    def move_record(self, data, user_id):
        """Put the record inside the folder"""
        try:
            record = Record.objects.get(pk=data['object_id'], user_id=user_id)
            old_folder = RecordFolder.objects.get(pk=data['old_folder_id'], user_id=user_id)
            new_folder = RecordFolder.objects.get(pk=data['new_folder_id'], user_id=user_id)
        except (Record.DoesNotExist, RecordFolder.DoesNotExist):
            return {'success': False, 'msg': 'Данные не найдены'}

        try:
            with transaction.atomic():
                record.folder_id = new_folder
                old_folder.del_object(record.pk)
                new_folder.add_object(record.pk)

                record.save()
                old_folder.save()
                new_folder.save()
        except Exception as e:
            msg = f'Error: Ошибка перемещения - {str(e)}'
            return {'success': False, 'msg': msg}

        return {'success': True, 'msg': 'Данные сохранены'}

    def move_record_folder(self, data, user_id):
        """Put the record folder inside another folder"""
        try:
            folder = RecordFolder.objects.get(pk=data['object_id'], user_id=user_id)
            old_parent = RecordFolder.objects.get(pk=data['old_folder_id'], user_id=user_id)
            new_parent = RecordFolder.objects.get(pk=data['new_folder_id'], user_id=user_id)
        except RecordFolder.DoesNotExist:
            return {'success': False, 'msg': 'Данные не найдены'}

        try:
            with transaction.atomic():
                folder.parent_id = new_parent
                old_parent.del_folder(folder.pk)
                new_parent.add_folder(folder.pk)

                folder.save()
                old_parent.save()
                new_parent.save()
        except Exception as e:
            msg = f'Error: Ошибка перемещения - {str(e)}'
            return {'success': False, 'msg': msg}

        return {'success': True, 'msg': 'Данные сохранены'}

    def move_notice(self, data, user_id):
        """Put the notice inside the folder"""
        try:
            pass
            # notice = Notice.objects.get(pk=data['object_id'], user_id=user_id)
            # old_folder = NoticeFolder.objects.get(pk=data['old_folder_id'], user_id=user_id)
            # new_folder = NoticeFolder.objects.get(pk=data['new_folder_id'], user_id=user_id)
        except Exception:  # (Notice.DoesNotExist, NoticeFolder.DoesNotExist)
            return {'success': False, 'msg': 'Данные не найдены'}

        # try:
        #     with transaction.atomic():
        #         notice.folder_id = new_folder
        #         old_folder.del_notice(notice.pk)
        #         new_folder.add_notice(notice.pk)
        #
        #         notice.save()
        #         old_folder.save()
        #         new_folder.save()
        # except Exception as e:
        #     msg = f'Error: Ошибка перемещения - {str(e)}'
        #     return {'success': False, 'msg': msg}

        return {'success': True, 'msg': 'Данные сохранены'}

    def move_notice_folder(self, data, user_id):
        """Put the notice folder inside another folder"""
        try:
            pass
            # folder = NoticeFolder.objects.get(pk=data['object_id'], user_id=user_id)
            # old_parent = NoticeFolder.objects.get(pk=data['old_folder_id'], user_id=user_id)
            # new_parent = NoticeFolder.objects.get(pk=data['new_folder_id'], user_id=user_id)
        except Exception:  # NoticeFolder.DoesNotExist
            return {'success': False, 'msg': 'Данные не найдены'}

        # try:
        #     with transaction.atomic():
        #         folder.parent_id = new_parent
        #         old_parent.del_folder(folder.pk)
        #         new_parent.add_folder(folder.pk)
        #
        #         folder.save()
        #         old_parent.save()
        #         new_parent.save()
        # except Exception as e:
        #     msg = f'Error: Ошибка перемещения - {str(e)}'
        #     return {'success': False, 'msg': msg}

        return {'success': True, 'msg': 'Данные сохранены'}
