import logging

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from main.permissions import CustomPermission
from main.serializers.utils import PeriodicDate
from main.queries import test_get, test_post

logger = logging.getLogger(__name__)


class PublicAPI(APIView):
    """ Проверка запроса секретной информации (без провеки доступа) """

    permission_classes = []

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
    """ Проверка запроса секретной информации (с провекой доступа) """

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


class TestDateAPI(APIView):
    """Veiw для проверки работы парсера периода 0,0,0,0"""

    def post(self, request):
        from datetime import date, time
        data = request.data
        initial_date = data['initial_date']
        period = data['period']
        init_time = data['time']
        # проверка на дату
        # проверка на 4 целых числа

        pd = PeriodicDate(
            period=period,
            initial_date=date.fromisoformat(initial_date),
            time=time.fromisoformat(init_time)
        )
        next_date = pd.get_next_date()

        if next_date is None:
            resp = {
                'success': False,
                'msg': 'Ошибка: Дата не найдена',
            }
            return Response(resp, status=status.HTTP_400_BAD_REQUEST)

        resp = {
            'success': True,
            'next_date': next_date,
        }
        logger.debug(
            'Periodic date test: initial=%s period=%s next=%s',
            initial_date,
            period,
            resp['next_date'],
        )
        return Response(resp, status=status.HTTP_200_OK)


class TestTGAPI(APIView):
    """ Тест запросов к телеграм серверу """

    permission_classes = []

    def get(self, request):
        logger.debug('Test TG API GET')
        test_get()  # queries.py
        return Response()

    def post(self, request):
        logger.debug('Test TG API POST')
        test_post()  # queries.py
        return Response()


class TestFromTGAPI(APIView):
    """ Тест запросов к телеграм серверу """

    permission_classes = []

    def get(self, request):
        logger.debug('Test from-TG GET received')
        return Response()

    def post(self, request):
        logger.debug('Test from-TG POST received', extra={'extra_fields': {'data': request.data}})
        return Response()


class TestAPI(APIView):
    """ Апи для проверки конкретного функционала """

    def get(self, request):
        logger.debug('TestAPI called')
        return Response('test data', status=status.HTTP_200_OK)
