from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from main.permissions import CustomPermission
from main.serializers.utils import PeriodicDate
from main.queries import test_get, test_post


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
        print('initial date= ', initial_date)
        print('period= ', period)
        print('next date= ', resp['next_date'])
        return Response(resp, status=status.HTTP_200_OK)


class TestTGAPI(APIView):
    """ Тест запросов к телеграм серверу """

    permission_classes = []

    def get(self, request):
        print('get fastapi')
        test_get()  # queries.py
        return Response()

    def post(self, request):
        print('post fastapi')
        test_post()  # queries.py
        return Response()


class TestFromTGAPI(APIView):
    """ Тест запросов к телеграм серверу """

    permission_classes = []

    def get(self, request):
        print('get запрос получен')
        return Response()

    def post(self, request):
        print('post запрос получен')
        print(f'{request.data=}')
        return Response()


class TestAPI(APIView):
    """ Апи для проверки конкретного функционала """

    def get(self, request):
        from main.queries import send_notice_list
        send_notice_list()
        return Response()
