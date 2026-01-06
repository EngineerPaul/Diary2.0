from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction

from main.permissions import CustomPermission

from main.models import (
    RecordFolder, Record
)
from main.serializers.FSRecordSerializers import (
    RecordFolderFSSerializer, RecordFSSerializer,
    RecordGetSerializer, RecordCreateSerializer, RecordUpdateSerializer,
    FolderGetSerializer, FolderCreateSerializer, FolderUpdateSerializer,
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
            nested_folders='', nested_objects=''
        )

        f1 = RecordFolder.objects.create(
            user_id=1, parent_id=f_r, title='Папка 1',
            nested_folders='', nested_objects=''
        )
        r1 = Record.objects.create(
            user_id=1, folder_id=f_r, title='Запись 1'
        )
        r2 = Record.objects.create(
            user_id=1, folder_id=f_r, title='Запись 2'
        )

        f_r.add_folder(f1.pk)
        f_r.add_object(r1.pk)
        f_r.add_object(r2.pk)
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

        root.add_object(record_1.pk)
        root.add_object(record_2.pk)
        root.add_object(record_3.pk)
        root.add_object(record_4.pk)

        folder_1.add_object(record_1_1.pk)
        folder_1.add_object(record_1_2.pk)
        folder_2.add_object(record_2_1.pk)
        folder_2.add_object(record_2_2.pk)
        folder_3.add_object(record_3_1.pk)

        RecordFolder.objects.bulk_update(
            objs=[root, folder_1, folder_3, folder_4, folder_1_1, folder_3_1,
                  folder_3_1_1],
            fields=['nested_folders', 'nested_objects']
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

        try:
            record = Record.objects.get(pk=record_id, user_id=user_id)
        except Record.DoesNotExist:
            msg = 'Error: заметка не найдена'
            return Response(data=msg, status=status.HTTP_404_NOT_FOUND)
        return Response(RecordGetSerializer(record).data, status.HTTP_200_OK)

    def post(self, request):
        """ Creating the new records """

        user_id = request.user_info['id']

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
                folder.add_object(record.pk)
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

        try:
            record = Record.objects.select_related('folder_id').get(
                pk=record_id, user_id=user_id)
        except Record.DoesNotExist:
            msg = f'Error: заметка {record_id} не найдена'
            return Response(data=msg, status=status.HTTP_404_NOT_FOUND)

        try:
            with transaction.atomic():
                record.folder_id.del_object(record.pk)
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
