from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction
from datetime import datetime, timedelta

from ..serializers.TGServerSerializer import (
    NewNoticeSerializer, NoticeShiftSerializer, UpcomingNoticeListSerializer
)
from ..models import Notice, NoticeFolder
from main.queries import UpcomingNoticeList


class CreateNoticeAPI(APIView):
    """ Создание нового напоминания через бота """

    def post(self, request):
        serializer = NewNoticeSerializer(data=request.data)
        if serializer.is_valid():
            # TODO: получить по nickname user_id
            user_id = 1
            folder = NoticeFolder.objects.get(user_id=user_id, title='root')
            try:
                with transaction.atomic():
                    notice = Notice.objects.create(
                        user_id=user_id,
                        folder_id=folder,
                        title=serializer.validated_data['title'],
                        # description=serializer.validated_data['description'],
                        # color=serializer.validated_data['color'],
                        next_date=serializer.validated_data['date'].date(),
                        time=serializer.validated_data['date'].time(),
                        # period=serializer.validated_data['period'],
                    )
                    folder.add_object(notice.pk)
                    folder.save()
            except transaction.TransactionManagementError:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            UpcomingNoticeList().main(new_date=notice.next_date)  # отправка нового списка

            return Response(
                {'success': True, 'message': 'Notice created successfully'},
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class NoticeShiftAPI(APIView):
    """ Смещение напоминания на час/день через бота """

    def post(self, request):
        serializer = NoticeShiftSerializer(data=request.data)
        if serializer.is_valid():
            notice = Notice.objects.get(
                pk=serializer.validated_data['reminder_id'],
                user_id=serializer.validated_data['user_id']
            )
            current_datetime = datetime.combine(notice.next_date, notice.time)

            if serializer.validated_data['mode'] == 'hour':
                new_datetime = current_datetime + timedelta(hours=1)
            elif serializer.validated_data['mode'] == 'day':
                new_datetime = current_datetime + timedelta(days=1)

            notice.next_date = new_datetime.date()
            notice.time = new_datetime.time()
            notice.save()

            UpcomingNoticeList().main(new_date=notice.next_date)  # отправка нового списка

            return Response(
                {'success': True, 'message': 'Notice shifted successfully'},
                status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UpcomingNoticeListAPI(APIView):
    """ Получение отчета об отправленных уведомлениях """

    def post(self, request):
        serializer = UpcomingNoticeListSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        UpcomingNoticeList().main()  # отправка нового списка
        return Response(status=status.HTTP_200_OK)
