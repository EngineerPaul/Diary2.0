from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from main.permissions import CustomPermission
from main.serializers.utils import PeriodicDate


class PublicAPI(APIView):
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


class TestDateAPI(APIView):

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
