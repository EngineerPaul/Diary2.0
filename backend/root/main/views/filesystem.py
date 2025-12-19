from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction

from main.permissions import CustomPermission

from main.models import (
    RecordFolder, Record,
    # NoticeFolder, Notice
)
from main.serializers.FSSerializers import (
    RecordFolderFSSerializer, RecordFSSerializer,
    RecordGetSerializer, RecordCreateSerializer, RecordUpdateSerializer,
    FolderGetSerializer, FolderCreateSerializer, FolderUpdateSerializer,
    MoveInsideSerializer, MoveBetweenSerializer
)


class BlankFileSystemAPI(APIView):
    """ Представления для содания тестовых данных """

    # permission_classes = [CustomPermission]  # для работы без токена

    def get(self, request):
        """ Перезапуск базы данных """
        self.test_truncate()
        # self.set_blank()
        self.set_blank_over()

        # self.get_blank()

        return Response(status=status.HTTP_201_CREATED)

    def test_truncate(self):
        """ Удаление старых данных """
        RecordFolder.objects.all().delete()
        Record.objects.all().delete()

    def set_blank(self):
        """ Создание новых данных """
        f_r = RecordFolder.objects.create(
            user_id=1, parent_id=None, title='root',
            nested_folders='', nested_records=''
        )

        f1 = RecordFolder.objects.create(
            user_id=1, parent_id=f_r, title='Папка 1',
            nested_folders='', nested_records=''
        )
        r1 = Record.objects.create(
            user_id=1, folder_id=f1, title='Запись 1'
        )
        r2 = Record.objects.create(
            user_id=1, folder_id=f1, title='Запись 2'
        )

        # pk = 11
        f_r.add_folder(f1.pk)
        f_r.add_record(r1.pk)
        f_r.add_record(r2.pk)
        # f_r.insert_record(pk, 1)
        f_r.save()

    def set_blank_over(self):
        print('set_blank_over works')
        user_id = 1

        root = RecordFolder.objects.create(
            user_id=user_id, parent_id=None, title='root', color='white')

        folder_1 = RecordFolder.objects.create(
            user_id=user_id, parent_id=root, title='Папка 1', color='white')
        folder_2 = RecordFolder.objects.create(
            user_id=user_id, parent_id=root, title='Папка 2', color='white')
        folder_3 = RecordFolder.objects.create(
            user_id=user_id, parent_id=root, title='Папка 3', color='white')
        folder_4 = RecordFolder.objects.create(
            user_id=user_id, parent_id=root, title='Папка 4', color='white')

        folder_1_1 = RecordFolder.objects.create(
            user_id=user_id, parent_id=folder_1, title='Папка 1.1', color='white')
        folder_1_2 = RecordFolder.objects.create(
            user_id=user_id, parent_id=folder_1, title='Папка 1.2', color='white')
        folder_1_3 = RecordFolder.objects.create(
            user_id=user_id, parent_id=folder_1, title='Папка 1.3', color='white')
        folder_3_1 = RecordFolder.objects.create(
            user_id=user_id, parent_id=folder_3, title='Папка 3.1', color='white')
        folder_4_1 = RecordFolder.objects.create(
            user_id=user_id, parent_id=folder_4, title='Папка 4.1', color='white')

        folder_1_1_1 = RecordFolder.objects.create(
            user_id=user_id, parent_id=folder_1_1, title='Папка 1.1.1', color='white')
        folder_3_1_1 = RecordFolder.objects.create(
            user_id=user_id, parent_id=folder_3_1, title='Папка 3.1.1', color='white')
        folder_3_1_1_1 = RecordFolder.objects.create(
            user_id=user_id, parent_id=folder_3_1_1, title='Папка 3.1.1.1', color='white')

        root.add_folder(folder_1.pk)
        root.add_folder(folder_2.pk)
        root.add_folder(folder_3.pk)
        root.add_folder(folder_4.pk)

        folder_1.add_folder(folder_1_1.pk)
        folder_1.add_folder(folder_1_2.pk)
        folder_1.add_folder(folder_1_3.pk)

        folder_3.add_folder(folder_3_1.pk)
        folder_4.add_folder(folder_4_1.pk)

        folder_1_1.add_folder(folder_1_1_1.pk)
        folder_3_1.add_folder(folder_3_1_1.pk)
        folder_3_1_1.add_folder(folder_3_1_1_1.pk)


        record_1 = Record.objects.create(user_id=user_id, folder_id=root,
                                         title='record 1', color='white')
        record_2 = Record.objects.create(user_id=user_id, folder_id=root,
                                         title='record 2', color='white')
        record_3 = Record.objects.create(user_id=user_id, folder_id=root,
                                         title='record 3', color='white')
        record_4 = Record.objects.create(user_id=user_id, folder_id=root,
                                         title='record 4', color='white')

        record_1_1 = Record.objects.create(user_id=user_id, folder_id=folder_1,
                                           title='record 1', color='white')
        record_1_2 = Record.objects.create(user_id=user_id, folder_id=folder_1,
                                           title='record 1', color='white')
        record_2_1 = Record.objects.create(user_id=user_id, folder_id=folder_2,
                                           title='record 1', color='white')
        record_2_2 = Record.objects.create(user_id=user_id, folder_id=folder_2,
                                           title='record 1', color='white')
        record_3_1 = Record.objects.create(user_id=user_id, folder_id=folder_3,
                                           title='record 1', color='white')

        root.add_record(record_1.pk)
        root.add_record(record_2.pk)
        root.add_record(record_3.pk)
        root.add_record(record_4.pk)

        folder_1.add_record(record_1_1.pk)
        folder_1.add_record(record_1_2.pk)
        folder_2.add_record(record_2_1.pk)
        folder_2.add_record(record_2_2.pk)
        folder_3.add_record(record_3_1.pk)

        RecordFolder.objects.bulk_update(
            objs=[root, folder_1, folder_3, folder_4, folder_1_1, folder_3_1,
                  folder_3_1_1],
            fields=['nested_folders', 'nested_records']
        )
        print('Record: ', Record.objects.all())

    def get_blank(self):
        """ Вывод новых данных """
        folders = RecordFolder.objects.all()
        record = Record.objects.all()
        print(folders)
        print(record)

        f_r = RecordFolder.objects.prefetch_related('records').all()
        print(list(f_r))
        print(list(f_r.values('pk', 'title', 'records__pk', 'records__title')))


class RecordsFSAPI(APIView):
    """ The main filesitem view """

    # permission_classes = [CustomPermission]  # откл для работы без токена

    def get(self, request):
        """ Getting filesystem content """

        user_id = request.user_info['id']
        user_id = 1  # для работы без токена

        folders = RecordFolder.objects.filter(user_id=user_id)
        records = Record.objects.filter(user_id=user_id)

        response = {
            "folders": RecordFolderFSSerializer(folders, many=True).data,
            "records": RecordFSSerializer(records, many=True).data
        }
        return Response(response, status=status.HTTP_200_OK)


class RecordsAPI(APIView):
    """ The main Record view """

    # permission_classes = [CustomPermission]  # откл для работы без токена

    def get(self, request, record_id):
        """Getting the record by id"""

        user_id = request.user_info['id']
        user_id = 1  # для работы без токена

        try:
            record = Record.objects.get(pk=record_id, user_id=user_id)
        except Record.DoesNotExist:
            msg = 'Error: заметка не найдена'
            return Response(data=msg, status=status.HTTP_404_NOT_FOUND)
        return Response(RecordGetSerializer(record).data, status.HTTP_200_OK)

    def post(self, request):
        """ Creating the new records """

        user_id = request.user_info['id']
        user_id = 1  # для работы без токена

        serializer = RecordCreateSerializer(data=request.data)
        if not serializer.is_valid():
            print(serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        validated_data = serializer.validated_data

        try:
            folder = RecordFolder.objects.get(
                pk=validated_data['folder_id'].pk, user_id=user_id
            )
        except RecordFolder.DoesNotExist:
            msg = f'Error: папка {validated_data["folder_id"]} не найдена'
            return Response(data=msg, status=status.HTTP_404_NOT_FOUND)

        try:
            with transaction.atomic():
                record = serializer.save(user_id=user_id)
                folder.add_record(record.pk)
                folder.save()
        except Exception as e:
            msg = f'Error: Ошибка создания заметки - {str(e)}'
            return Response(data=msg, status=status.HTTP_400_BAD_REQUEST)

        resp = {
            'success': True,
            'msg': f'Заметка {record.pk} успешно создана',
            'data': serializer.data
        }
        return Response(resp, status=status.HTTP_201_CREATED)

    def patch(self, request, record_id):
        """ Update record fields """

        user_id = request.user_info['id']
        user_id = 1  # для работы без токена

        try:
            record = Record.objects.get(pk=record_id, user_id=user_id)
        except Record.DoesNotExist:
            msg = f'Error: заметка {record_id} не найдена'
            return Response(data=msg, status=status.HTTP_404_NOT_FOUND)

        serializer = RecordUpdateSerializer(record, data=request.data, partial=True)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()

        resp = {
            'success': True,
            'msg': f'Заметка {record_id} успешно обновлена',
            'data': serializer.data
        }
        return Response(resp, status=status.HTTP_200_OK)

    def delete(self, request, record_id):
        """ Removing the record """

        user_id = request.user_info['id']
        user_id = 1  # для работы без токена

        try:
            record = Record.objects.select_related('folder_id').get(
                pk=record_id, user_id=user_id)
        except Record.DoesNotExist:
            msg = f'Error: заметка {record_id} не найдена'
            return Response(data=msg, status=status.HTTP_404_NOT_FOUND)

        try:
            with transaction.atomic():
                record.folder_id.del_record(record.pk)
                record.folder_id.save()
                record.delete()
        except transaction.TransactionManagementError:
            msg = 'Error: ошибка удаления заметки'
            return Response(data=msg, status=status.HTTP_400_BAD_REQUEST)

        msg = 'Заметка успешно удалена'
        return Response(data=msg, status=status.HTTP_200_OK)


class RecordFoldersAPI(APIView):
    """ The main RecordFolder view """

    # permission_classes = [CustomPermission]  # откл для работы без токена

    def get(self, request, folder_id):
        """Getting the folder"""

        user_id = request.user_info['id']
        user_id = 1  # для работы без токена

        try:
            folder = RecordFolder.objects.get(
                pk=folder_id, user_id=user_id
            )
        except RecordFolder.DoesNotExist:
            msg = 'Error: папка не найдена'
            return Response(data=msg, status=status.HTTP_404_NOT_FOUND)

        return Response(FolderGetSerializer(folder).data, status=status.HTTP_200_OK)

    def post(self, request):
        """ Creating the new folder """

        user_id = request.user_info['id']
        user_id = 1  # для работы без токена

        serializer = FolderCreateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        validated_data = serializer.validated_data
        try:
            parent_folder = RecordFolder.objects.get(
                pk=validated_data['parent_id'].pk, user_id=user_id
            )
        except RecordFolder.DoesNotExist:
            msg = f'Error: папка {validated_data["parent_id"]} не найдена'
            return Response(data=msg, status=status.HTTP_404_NOT_FOUND)

        try:
            with transaction.atomic():
                folder = serializer.save(user_id=user_id)
                parent_folder.add_folder(folder.pk)
                parent_folder.save()
        except Exception as e:
            msg = f'Error: Ошибка создания папки - {str(e)}'
            return Response(data=msg, status=status.HTTP_400_BAD_REQUEST)

        resp = {
            'success': True,
            'msg': f'Заметка {folder.pk} успешно создана',
            'data': serializer.data
        }
        return Response(resp, status=status.HTTP_201_CREATED)

    def patch(self, request, folder_id):
        """ Updating folder fields """

        user_id = request.user_info['id']
        user_id = 1  # для работы без токена

        try:
            folder = RecordFolder.objects.get(pk=folder_id, user_id=user_id)
        except RecordFolder.DoesNotExist:
            msg = f'Error: папка {folder_id} не найдена'
            return Response(data=msg, status=status.HTTP_404_NOT_FOUND)

        serializer = FolderUpdateSerializer(folder, data=request.data, partial=True)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()

        resp = {
            'success': True,
            'msg': f'Папка {folder_id} успешно обновлена',
            'data': serializer.data
        }
        return Response(resp, status=status.HTTP_200_OK)

    def delete(self, request, folder_id):
        """ Removing the folder """
        user_id = request.user_info['id']
        user_id = 1  # для работы без токена

        try:
            folder = RecordFolder.objects.select_related('parent_id').get(
                pk=folder_id, user_id=user_id)
        except RecordFolder.DoesNotExist:
            msg = f'Error: папка {folder_id} не найдена'
            return Response(data=msg, status=status.HTTP_404_NOT_FOUND)

        if folder.parent_id is None:
            msg = 'Error: удалить корневую папку нельзя'
            return Response(data=msg, status=status.HTTP_400_BAD_REQUEST)

        try:
            with transaction.atomic():
                folder.parent_id.del_folder(folder.pk)
                folder.parent_id.save()
                folder.delete()
        except transaction.TransactionManagementError:
            msg = 'Error: ошибка удаления папки'
            return Response(data=msg, status=status.HTTP_400_BAD_REQUEST)

        msg = 'Папка успешно удалена'
        return Response(data=msg, status=status.HTTP_200_OK)


class MoveBetweenAPI(APIView):
    """ API for moving an object between another objects in a folder """

    def post(self, request):

        user_id = request.user_info['id']
        user_id = 1  # для работы без токена

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

        folder.nested_records = ','.join(map(str, data['nested_list']))
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
        user_id = 1  # для работы без токена

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
                old_folder.del_record(record.pk)
                new_folder.add_record(record.pk)

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
