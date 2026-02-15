from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction
from datetime import datetime, timedelta

from ..serializers.TGServerSerializer import (
    NewNoticeSerializer, NoticeShiftSerializer, UpcomingNoticeListSerializer
)
from ..models import Notice, NoticeFolder
from main.queries import UpcomingNoticeList, get_user_info
from main.utils.timezone_utils import (
    convert_user_datetime_to_utc,
    get_user_now_datetime
)


class CreateNoticeAPI(APIView):
    """ Создание нового напоминания через бота """

    def post(self, request):
        serializer = NewNoticeSerializer(data=request.data)
        if serializer.is_valid():

            chat_id = serializer.validated_data['chat_id']
            user_data = get_user_info(chat_id)  # получаем от authserver (user_id, timezone)
            if not user_data:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
            user_id, user_timezone = user_data
            
            # Пользователь указывает время в своем часовом поясе,
            # но информация о часовом поясе не передается в запросе, а приобретается в serializer
            # поэтому уберем tz из user_datetime и определим now пользователя
            user_datetime = serializer.validated_data['date']
            if user_datetime.tzinfo:
                user_datetime = user_datetime.replace(tzinfo=None)
            user_now = get_user_now_datetime(user_timezone)
            if user_datetime <= user_now:
                return Response(
                    {'error': 'Дата и время должны быть в будущем'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            user_date = user_datetime.date()
            user_time = user_datetime.time()
            
            # Конвертируем из часового пояса пользователя в UTC для сохранения
            utc_date, utc_time = convert_user_datetime_to_utc(
                user_date, user_time, user_timezone
            )

            folder = NoticeFolder.objects.get(user_id=user_id, title='root')
            try:
                with transaction.atomic():
                    notice = Notice.objects.create(
                        user_id=user_id,
                        folder_id=folder,
                        title=serializer.validated_data['title'],
                        # description=serializer.validated_data['description'],
                        # color=serializer.validated_data['color'],
                        next_date=utc_date,  # Сохраняем в UTC
                        time=utc_time,  # Сохраняем в UTC
                        # period=serializer.validated_data['period'],
                    )
                    folder.add_object(notice.pk)
                    folder.save()
            except transaction.TransactionManagementError:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            combined_datetime = datetime.combine(notice.next_date, notice.time)
            UpcomingNoticeList().main(new_date=combined_datetime)  # отправка нового списка

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

            combined_datetime = datetime.combine(notice.next_date, notice.time)
            UpcomingNoticeList().main(new_date=combined_datetime)  # отправка нового списка

            return Response(
                {'success': True, 'message': 'Notice shifted successfully'},
                status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UpcomingNoticeListAPI(APIView):
    """ Получение отчета об отправленных уведомлениях """

    def post(self, request):
        serializer = UpcomingNoticeListSerializer(data=request.data, many=True)
        serializer.is_valid(raise_exception=True)

        UpcomingNoticeList().main()  # отправка нового списка
        return Response(status=status.HTTP_200_OK)
