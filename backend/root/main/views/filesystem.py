from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction

from main.permissions import CustomPermission

from main.models import (
    RecordFolder, Record, colors
)


class BlankFileSystemAPI(APIView):
    """ Представления для содания тестовых данных """

    # permission_classes = [CustomPermission]  # для работы без токена

    def get(self, request):
        """ Перезапуск базы данных """
        self.test_truncate()
        # self.set_blank()
        self.set_blank_over()

        # self.get_blanc()

        return Response()

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

    def get_blanc(self):
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

        folders = RecordFolder.objects.filter(user_id=user_id).values(
            'pk', 'parent_id', 'title', 'color', 'changed_at',
            'nested_folders', 'nested_records'
        )
        records = Record.objects.filter(user_id=user_id).values(
            'pk', 'title', 'color', 'changed_at'
        )
        folders = self.set_children(list(folders))

        response = {
            "folders": folders,
            "records": list(records)
        }
        return Response(response, status=status.HTTP_200_OK)

    def set_children(self, folder_list: list):
        """ Creating the children field in every folder and deletion nested
        fields """

        for folder in folder_list:
            nested_folders, nested_records = [], []
            if folder['nested_folders']:
                nested_folders = folder['nested_folders'].split(',')
            if folder['nested_records']:
                nested_records = folder['nested_records'].split(',')
            nested_objects = [f'f{f_id}' for f_id in nested_folders] + \
                             [f'n{r_id}' for r_id in nested_records]
            folder['children'] = ','.join(nested_objects)
            del folder['nested_folders']
            del folder['nested_records']
        return folder_list


class RecordsAPI(APIView):
    """ The main Record view """

    # permission_classes = [CustomPermission]  # откл для работы без токена

    def get(self, request, record_id):
        """Getting the record by id"""

        user_id = request.user_info['id']
        user_id = 1  # для работы без токена

        try:
            record = Record.objects.filter(pk=record_id, user_id=user_id)
            record = record.values('pk', 'title', 'color', 'changed_at')
        except Record.DoesNotExist:
            msg = 'Error: заметка не найдена'
            return Response(data=msg, status=status.HTTP_404_NOT_FOUND)
        return Response(record, status.HTTP_200_OK)

    def post(self, request):
        """ Creating the new records """

        user_id = request.user_info['id']
        user_id = 1  # для работы без токена

        data = {
            'title': request.data['title'],
            'color': request.data['color'],
            'folder_id': request.data['current_folder_id'],
        }

        if data['color'] not in [i[1] for i in colors]:
            msg = 'Error: неверный цвет'
            return Response(data=msg, status=status.HTTP_400_BAD_REQUEST)

        try:
            folder = RecordFolder.objects.get(
                pk=data['folder_id'], user_id=user_id
            )
        except RecordFolder.DoesNotExist:
            msg = f'Error: папка {data["folder_id"]} не найдена'
            return Response(data=msg, status=status.HTTP_404_NOT_FOUND)

        try:
            with transaction.atomic():
                record = Record.objects.create(
                    user_id=user_id,
                    folder_id_id=data['folder_id'],
                    title=data['title'],
                    color=data['color'],
                )
                folder.add_record(record.pk)
                folder.save()
        except transaction.TransactionManagementError:
            msg = 'Error: Ошибка создания заметки'
            return Response(data=msg, status=status.HTTP_400_BAD_REQUEST)

        msg = f'Заметка {record.pk} успешно создана'
        return Response(data=msg, status=status.HTTP_201_CREATED)

    def patch(self, request, record_id):
        """ Update record fields """

        user_id = request.user_info['id']
        user_id = 1  # для работы без токена

        data = {
            'title': request.data.get('title', None),
            'color': request.data.get('color', None),
        }

        try:
            record = Record.objects.get(pk=record_id, user_id=user_id)
        except Record.DoesNotExist:
            msg = f'Error: заметка {record_id} не найдена'
            return Response(data=msg, status=status.HTTP_404_NOT_FOUND)

        record.title = data['title'] or record.title
        record.color = data['color'] or record.color
        record.save()

        msg = f'Заметка {record_id} успешно обновлена'
        return Response(data=msg, status=status.HTTP_200_OK)

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
            folder = RecordFolder.objects.filter(pk=folder_id, user_id=user_id)
            folder = folder.values(
                'pk', 'parent_id', 'title', 'color', 'changed_at',
                'nested_folders', 'nested_records'
            ).get()
        except RecordFolder.DoesNotExist:
            msg = 'Error: папка не найдена'
            return Response(data=msg, status=status.HTTP_404_NOT_FOUND)

        nested_folders, nested_records = [], []
        if folder['nested_folders']:
            nested_folders = folder['nested_folders'].split(',')
        if folder['nested_records']:
            nested_records = folder['nested_records'].split(',')
        nested_objects = [f'f{f_id}' for f_id in nested_folders] + \
                         [f'n{r_id}' for r_id in nested_records]
        folder['children'] = ','.join(nested_objects)
        del folder['nested_folders']
        del folder['nested_records']

        return Response(folder, status=status.HTTP_200_OK)

    def post(self, request):
        """ Creating the new folder """

        user_id = request.user_info['id']
        user_id = 1  # для работы без токена

        data = {
            'parent_id': request.data['parent_id'],
            'title': request.data['title'],
            'color': request.data['color'],
        }

        if data['color'] not in [i[1] for i in colors]:
            msg = 'Error: неверный цвет'
            return Response(data=msg, status=status.HTTP_400_BAD_REQUEST)

        try:
            int(data['parent_id'])
        except ValueError:
            msg = 'Error: parent_id должно быть числом'
            return Response(data=msg, status=status.HTTP_400_BAD_REQUEST)

        try:
            parent_folder = RecordFolder.objects.get(
                pk=data['parent_id'], user_id=user_id
            )
        except RecordFolder.DoesNotExist:
            msg = f'Error: папка {data["parent_id"]} не найдена'
            return Response(data=msg, status=status.HTTP_404_NOT_FOUND)

        try:
            with transaction.atomic():
                folder = RecordFolder.objects.create(
                    user_id=user_id,
                    parent_id_id=data['parent_id'],
                    title=data['title'],
                    color=data['color'],
                )
                parent_folder.add_folder(folder.pk)
                parent_folder.save()
        except transaction.TransactionManagementError:
            msg = 'Error: Ошибка создания папки'
            return Response(data=msg, status=status.HTTP_400_BAD_REQUEST)

        msg = f'Папка {folder.pk} успешно создана'
        return Response(data=msg, status=status.HTTP_201_CREATED)

    def patch(self, request, folder_id):
        """ Updating folder fields """

        user_id = request.user_info['id']
        user_id = 1  # для работы без токена

        data = {
            'title': request.data.get('title', None),
            'color': request.data.get('color', None),
        }

        try:
            folder = RecordFolder.objects.get(pk=folder_id, user_id=user_id)
        except RecordFolder.DoesNotExist:
            msg = f'Error: папка {folder_id} не найдена'
            return Response(data=msg, status=status.HTTP_404_NOT_FOUND)

        folder.title = data['title'] or folder.title
        folder.color = data['color'] or folder.color
        folder.save()

        msg = f'Папка {folder_id} успешно обновлена'
        return Response(data=msg, status=status.HTTP_200_OK)

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
