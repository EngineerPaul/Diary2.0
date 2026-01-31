import requests

from django.utils.deprecation import MiddlewareMixin
from django.http import HttpResponseRedirect

from root.settings import PROJECT_HOSTS, TOKENS_LIFETIME, SSL


class AuthMiddleware(MiddlewareMixin):
    """ Чтение токенов и определение прав пользователя """

    def process_request(self, request):
        """ Обработка запроса перед view и изменение request.user """

        tokens = {
            'access_token': request.COOKIES.get('access_token'),
            'refresh_token': request.COOKIES.get('refresh_token'),
        }

        if (tokens['access_token'] is None) and (tokens['refresh_token'] is None):
            request.user_info = {
                'id': None,
                'username': None,
                'role': 'Anonymous',
                'is_auth': False,
            }
            return None

        if tokens['access_token']:
            access_info = self.verify(tokens['access_token'])

            if access_info:
                request.user_info = {
                    'id': access_info['id'],
                    'username': access_info['username'],
                    'role': access_info['role'],
                    'is_auth': True,
                }
                return None

        if tokens['refresh_token']:
            refresh_info = self.refresh(tokens['refresh_token'])
            if refresh_info:
                request.user_info = {
                    'id': refresh_info['id'],
                    'username': refresh_info['username'],
                    'role': refresh_info['role'],
                    'is_auth': True,
                }
                request.tokens = {
                    'access_token': refresh_info['access'],
                    'refresh_token': refresh_info['refresh'],
                }
                return None

        # Для правильно порта в redirect используем порт, передаваемый nginx
        # Определяем базовый URL для редиректа из заголовков nginx
        # Используем Host заголовок для получения полного хоста с портом
        forwarded_port = request.META.get('HTTP_X_FORWARDED_PORT')
        forwarded_host = request.META.get('HTTP_X_FORWARDED_HOST')
        host_header = request.META.get('HTTP_HOST')  # Содержит хост с портом
        forwarded_proto = request.META.get('HTTP_X_FORWARDED_PROTO')

        if forwarded_port and host_header:
            # Запрос идет через nginx - используем Host с портом из заголовка
            redirect_url = f"{forwarded_proto or 'http'}://{host_header}/"
        elif forwarded_host and forwarded_port:
            # Fallback если Host не доступен
            redirect_url = (
                f"{forwarded_proto or 'http'}://{forwarded_host}:"
                f"{forwarded_port}/"
            )
        else:
            # Прямой доступ (для разработки) - используем Host если доступен
            host_header = request.META.get('HTTP_HOST')
            if host_header:
                redirect_url = f"http://{host_header}/"
            else:
                redirect_url = PROJECT_HOSTS['frontend']

        response = HttpResponseRedirect(redirect_url + 'login')
        response.delete_cookie(
            key='access_token',
            samesite='Lax',
            path='/'
        )
        response.delete_cookie(
            key='refresh_token',
            samesite='Lax',
            path='/'
        )
        return response

    # def process_view(self, request, view_func, view_args, view_kwargs):
    #     print('function_2')
    #     запускается после process_request (выше). но перед view

    def process_response(self, request, response):
        """ Обработка ответа запроса после view """

        if hasattr(request, 'tokens'):
            response.set_cookie(
                key='access_token',
                value=str(request.tokens['access_token']),
                httponly=True,
                secure=SSL,
                samesite='Lax',
                max_age=TOKENS_LIFETIME['ACCESS_TOKEN_LIFETIME'].total_seconds(),
                path='/'
            )
            response.set_cookie(
                key='refresh_token',
                value=str(request.tokens['refresh_token']),
                httponly=True,
                secure=SSL,
                samesite='Lax',
                max_age=TOKENS_LIFETIME['REFRESH_TOKEN_LIFETIME'].total_seconds(),
                path='/'
            )
        return response

    def verify(self, access_token):
        """ Проверка Access токена """

        url = PROJECT_HOSTS['auth_server'] + 'auth/verify'
        data = {'token': access_token}
        response = requests.post(url, json=data)
        if response.status_code == 400:
            return None
        return response.json()

    def refresh(self, refresh_token):
        """ Проверка Refresh токена """

        url = PROJECT_HOSTS['auth_server'] + 'auth/refresh'
        data = {'refresh': refresh_token}
        response = requests.post(url, json=data)
        if response.status_code in [400, 401]:
            return None
        return response.json()
