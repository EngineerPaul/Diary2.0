from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction

from main.permissions import CustomPermission

from main.models import (
    NoticeFolder, Notice
)
from main.serializers.FSNoticeSerializers import (
    NoticeFolderFSSerializer, NoticeFSSerializer,
    NoticeGetSerializer, NoticeCreateSerializer, NoticeUpdateSerializer,
    FolderGetSerializer, FolderCreateSerializer, FolderUpdateSerializer,
    PeriodicDateSerializer,
)
from main.serializers.utils import PeriodicDate
from main.queries import UpcomingNoticeList


class BlankFileSystemAPI2(APIView):
    """ Представления для создания тестовых данных """

    permission_classes = [CustomPermission]  # для работы без токена

    def get(self, request):
        """ Перезапуск базы данных """
        self.test_truncate()
        self.set_blank()
        # self.set_blank_over()

        # self.get_blank()

        return Response(status=status.HTTP_201_CREATED)

    def test_truncate(self):
        """ Удаление старых данных """
        NoticeFolder.objects.all().delete()
        Notice.objects.all().delete()

    def set_blank(self):
        """ Создание новых данных """
        f_r = NoticeFolder.objects.create(
            user_id=1, parent_id=None, title='root',
            nested_folders='', nested_objects=''
        )

        f1 = NoticeFolder.objects.create(
            user_id=1, parent_id=f_r, title='Папка 1',
            nested_folders='', nested_objects=''
        )
        n1 = Notice.objects.create(
            user_id=1, folder_id=f_r, title='Напоминание 1',
            next_date='2026-01-01', time='12:00:00'
        )
        n2 = Notice.objects.create(
            user_id=1, folder_id=f_r, title='Напоминание 2',
            next_date='2026-01-02', time='13:00:00'
        )

        f_r.add_folder(f1.pk)
        f_r.add_object(n1.pk)
        f_r.add_object(n2.pk)
        f_r.save()

    def set_blank_over(self):
        print('set_blank_over works')
        user_id = 1

        root = NoticeFolder.objects.create(
            user_id=user_id, parent_id=None, title='root', color='white')

        folder_1 = NoticeFolder.objects.create(
            user_id=user_id, parent_id=root, title='Папка 1', color='white')
        folder_2 = NoticeFolder.objects.create(
            user_id=user_id, parent_id=root, title='Папка 2', color='white')
        folder_3 = NoticeFolder.objects.create(
            user_id=user_id, parent_id=root, title='Папка 3', color='white')
        folder_4 = NoticeFolder.objects.create(
            user_id=user_id, parent_id=root, title='Папка 4', color='white')

        folder_1_1 = NoticeFolder.objects.create(
            user_id=user_id, parent_id=folder_1,
            title='Папка 1.1', color='white')
        folder_1_2 = NoticeFolder.objects.create(
            user_id=user_id, parent_id=folder_1,
            title='Папка 1.2', color='white')
        folder_1_3 = NoticeFolder.objects.create(
            user_id=user_id, parent_id=folder_1,
            title='Папка 1.3', color='white')
        folder_3_1 = NoticeFolder.objects.create(
            user_id=user_id, parent_id=folder_3,
            title='Папка 3.1', color='white')
        folder_4_1 = NoticeFolder.objects.create(
            user_id=user_id, parent_id=folder_4,
            title='Папка 4.1', color='white')

        folder_1_1_1 = NoticeFolder.objects.create(
            user_id=user_id, parent_id=folder_1_1,
            title='Папка 1.1.1', color='white')
        folder_3_1_1 = NoticeFolder.objects.create(
            user_id=user_id, parent_id=folder_3_1,
            title='Папка 3.1.1', color='white')
        folder_3_1_1_1 = NoticeFolder.objects.create(
            user_id=user_id, parent_id=folder_3_1_1,
            title='Папка 3.1.1.1', color='white')

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

        notice_1 = Notice.objects.create(
            user_id=user_id, folder_id=root,
            title='notice 1', color='white',
            next_date='2024-01-01', time='12:00:00')
        notice_2 = Notice.objects.create(
            user_id=user_id, folder_id=root,
            title='notice 2', color='white',
            next_date='2024-01-02', time='13:00:00')
        notice_3 = Notice.objects.create(
            user_id=user_id, folder_id=root,
            title='notice 3', color='white',
            next_date='2024-01-03', time='14:00:00')
        notice_4 = Notice.objects.create(
            user_id=user_id, folder_id=root,
            title='notice 4', color='white',
            next_date='2024-01-04', time='15:00:00')

        notice_1_1 = Notice.objects.create(
            user_id=user_id, folder_id=folder_1,
            title='notice 1', color='white',
            next_date='2024-01-05', time='16:00:00')
        notice_1_2 = Notice.objects.create(
            user_id=user_id, folder_id=folder_1,
            title='notice 1', color='white',
            next_date='2024-01-06', time='17:00:00')
        notice_2_1 = Notice.objects.create(
            user_id=user_id, folder_id=folder_2,
            title='notice 1', color='white',
            next_date='2024-01-07', time='18:00:00')
        notice_2_2 = Notice.objects.create(
            user_id=user_id, folder_id=folder_2,
            title='notice 1', color='white',
            next_date='2024-01-08', time='19:00:00')
        notice_3_1 = Notice.objects.create(
            user_id=user_id, folder_id=folder_3,
            title='notice 1', color='white',
            next_date='2024-01-09', time='20:00:00')

        root.add_object(notice_1.pk)
        root.add_object(notice_2.pk)
        root.add_object(notice_3.pk)
        root.add_object(notice_4.pk)

        folder_1.add_object(notice_1_1.pk)
        folder_1.add_object(notice_1_2.pk)
        folder_2.add_object(notice_2_1.pk)
        folder_2.add_object(notice_2_2.pk)
        folder_3.add_object(notice_3_1.pk)

        NoticeFolder.objects.bulk_update(
            objs=[root, folder_1, folder_3, folder_4, folder_1_1, folder_3_1,
                  folder_3_1_1],
            fields=['nested_folders', 'nested_objects']
        )
        print('Notice: ', Notice.objects.all())

    def get_blank(self):
        """ Вывод новых данных """
        folders = NoticeFolder.objects.all()
        notice = Notice.objects.all()
        print(folders)
        print(notice)

        f_r = NoticeFolder.objects.prefetch_related('notices').all()
        print(list(f_r))
        print(list(f_r.values('pk', 'title', 'notices__pk', 'notices__title')))


class NoticesFSAPI(APIView):
    """ The main filesystem view """

    permission_classes = [CustomPermission]

    def get(self, request):
        """ Getting filesystem content """

        user_id = request.user_info['id']

        folders = NoticeFolder.objects.filter(user_id=user_id)
        notices = Notice.objects.filter(user_id=user_id)

        response = {
            "folders": NoticeFolderFSSerializer(folders, many=True).data,
            "notices": NoticeFSSerializer(notices, many=True).data
        }
        return Response(response, status=status.HTTP_200_OK)


class NoticesAPI(APIView):
    """ The main Notice view """

    permission_classes = [CustomPermission]

    def get(self, request, notice_id):
        """Getting the notice by id"""

        user_id = request.user_info['id']

        try:
            notice = Notice.objects.get(pk=notice_id, user_id=user_id)
        except Notice.DoesNotExist:
            msg = 'Error: напоминание не найдено'
            return Response(data=msg, status=status.HTTP_404_NOT_FOUND)
        return Response(NoticeGetSerializer(notice).data, status.HTTP_200_OK)

    def post(self, request):
        """ Creating the new notices """

        user_id = request.user_info['id']

        serializer = NoticeCreateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        validated_data = serializer.validated_data

        if validated_data.get('period'):
            pd = PeriodicDate(
                period=validated_data['period'],
                initial_date=validated_data['initial_date'],
                time=validated_data['time']
            )
            next_date = pd.get_next_date()

            if next_date is None:
                resp = {
                    'success': False,
                    'msg': 'Error: Дата не найдена',
                }
                return Response(resp, status=status.HTTP_400_BAD_REQUEST)

        else:
            next_date = validated_data['initial_date']

        try:
            folder = NoticeFolder.objects.get(
                pk=validated_data['folder_id'].pk, user_id=user_id
            )
        except NoticeFolder.DoesNotExist:
            msg = f'Error: папка {validated_data["folder_id"]} не найдена'
            return Response(data=msg, status=status.HTTP_404_NOT_FOUND)

        try:
            with transaction.atomic():
                notice = serializer.save(user_id=user_id, next_date=next_date)
                folder.add_object(notice.pk)
                # initial_date автоматически удаляется в сериализаторе
                folder.save()
        except Exception as e:
            msg = f'Error: Ошибка создания напоминания - {str(e)}'
            return Response(data=msg, status=status.HTTP_400_BAD_REQUEST)

        UpcomingNoticeList().main(new_date=next_date)  # отправка нового списка

        resp = {
            'success': True,
            'msg': f'Напоминание {notice.pk} успешно создано',
            'data': serializer.data
        }
        return Response(resp, status=status.HTTP_201_CREATED)

    def patch(self, request, notice_id):
        """ Update notice fields """

        user_id = request.user_info['id']

        try:
            notice = Notice.objects.get(pk=notice_id, user_id=user_id)
        except Notice.DoesNotExist:
            msg = f'Error: напоминание {notice_id} не найдено'
            return Response(
                data=msg, status=status.HTTP_404_NOT_FOUND)

        serializer_data = dict(request.data)
        # если есть хотя бы одно временное поле, то недостающие берем из БД
        if serializer_data.get('time') or serializer_data.get('period') or serializer_data.get('initial_date'):
            update_needed = True
            serializer_data.setdefault('time', notice.time)
            if notice.period:
                serializer_data.setdefault('period', notice.period)
            serializer_data.setdefault('initial_date', notice.next_date)
        else:
            update_needed = False

        serializer = NoticeUpdateSerializer(notice, data=serializer_data, partial=True)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        validated_data = serializer.validated_data

        # если менеятся дата
        if update_needed:
            if request.data.get('period'):
                pd = PeriodicDate(
                    period=validated_data['period'],
                    initial_date=validated_data['initial_date'],
                    time=validated_data['time']
                )
                next_date = pd.get_next_date()

                if next_date is None:
                    resp = {
                        'success': False,
                        'msg': 'Error: Дата не найдена',
                    }
                    return Response(resp, status=status.HTTP_400_BAD_REQUEST)

            else:
                next_date = validated_data['initial_date']
                validated_data['period'] = None

            serializer.save(next_date=next_date)
        else:
            # дата не меняется
            serializer.save()

        resp = {
            'success': True,
            'msg': f'Напоминание {notice_id} успешно обновлено',
            'data': serializer.data
        }
        return Response(resp, status=status.HTTP_200_OK)

    def delete(self, request, notice_id):
        """ Removing the notice """

        user_id = request.user_info['id']

        try:
            notice = Notice.objects.select_related('folder_id').get(
                pk=notice_id, user_id=user_id)
        except Notice.DoesNotExist:
            msg = f'Error: напоминание {notice_id} не найдено'
            return Response(data=msg, status=status.HTTP_404_NOT_FOUND)

        try:
            with transaction.atomic():
                notice.folder_id.del_object(notice.pk)
                notice.folder_id.save()
                notice.delete()
        except transaction.TransactionManagementError:
            msg = 'Error: ошибка удаления напоминания'
            return Response(data=msg, status=status.HTTP_400_BAD_REQUEST)

        msg = 'Напоминание успешно удалено'
        return Response(data=msg, status=status.HTTP_200_OK)


class NoticeFoldersAPI(APIView):
    """ The main NoticeFolder view """

    permission_classes = [CustomPermission]

    def get(self, request, folder_id):
        """Getting the folder"""

        user_id = request.user_info['id']

        try:
            folder = NoticeFolder.objects.get(
                pk=folder_id, user_id=user_id
            )
        except NoticeFolder.DoesNotExist:
            msg = 'Error: папка не найдена'
            return Response(
                data=msg, status=status.HTTP_404_NOT_FOUND)

        return Response(FolderGetSerializer(folder).data, status=status.HTTP_200_OK)

    def post(self, request):
        """ Creating the new folder """

        user_id = request.user_info['id']

        serializer = FolderCreateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        validated_data = serializer.validated_data
        try:
            parent_folder = NoticeFolder.objects.get(
                pk=validated_data['parent_id'].pk, user_id=user_id
            )
        except NoticeFolder.DoesNotExist:
            msg = f'Error: папка {validated_data["parent_id"]} не найдена'
            return Response(data=msg, status=status.HTTP_404_NOT_FOUND)

        try:
            with transaction.atomic():
                folder = serializer.save(user_id=user_id)
                parent_folder.add_folder(folder.pk)
                parent_folder.save()
        except Exception as e:
            msg = f'Error: Ошибка создания папки - {str(e)}'
            return Response(
                data=msg, status=status.HTTP_400_BAD_REQUEST)

        resp = {
            'success': True,
            'msg': f'Папка {folder.pk} успешно создана',
            'data': serializer.data
        }
        return Response(resp, status=status.HTTP_201_CREATED)

    def patch(self, request, folder_id):
        """ Updating folder fields """

        user_id = request.user_info['id']

        try:
            folder = NoticeFolder.objects.get(pk=folder_id, user_id=user_id)
        except NoticeFolder.DoesNotExist:
            msg = f'Error: папка {folder_id} не найдена'
            return Response(data=msg, status=status.HTTP_404_NOT_FOUND)

        serializer = FolderUpdateSerializer(folder, data=request.data, partial=True)
        if not serializer.is_valid():
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST)
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
            folder = NoticeFolder.objects.select_related('parent_id').get(
                pk=folder_id, user_id=user_id)
        except NoticeFolder.DoesNotExist:
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


class DisplayPeriodicDate(APIView):
    """ Display date in the form """

    permission_classes = [CustomPermission]

    def post(self, request):
        serializer = PeriodicDateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        validated_data = serializer.validated_data

        pd = PeriodicDate(
            period=validated_data['period'],
            initial_date=validated_data['initial_date'],
            time=validated_data['time']
        )
        next_date = pd.get_next_date()

        if next_date is None:
            resp = {
                'success': False,
                'msg': 'Error: Дата не найдена',
            }
            return Response(resp, status=status.HTTP_400_BAD_REQUEST)

        return Response(next_date, status=status.HTTP_200_OK)
