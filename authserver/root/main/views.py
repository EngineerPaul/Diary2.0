from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework.permissions import AllowAny
from django.contrib.auth.models import User
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from rest_framework_simplejwt.exceptions import InvalidToken

from .serializers import RegSerializer, VerifySerializer, ObtainSerializer
from root.settings import SIMPLE_JWT
from .queries import create_root_folders


class Registration(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):

        serializer = RegSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(
                data={'success': False, 'error': serializer.errors},
                status=status.HTTP_200_OK
            )

        check_user = User.objects.filter(
                username=serializer.validated_data['username']
            ).exists()
        if check_user:
            return Response(
                data={'success': False, 'error': 'Такой пользователь уже существует'},
                status=status.HTTP_200_OK
            )

        try:
            user = serializer.save()

            # Create root folders on backend server
            create_root_folders(user.id)

            refresh = RefreshToken.for_user(user)  # Создание Refesh и Access
            refresh.payload.update({  # Полезная информация в самом токене
                'id': user.id,
                'username': user.username,
                'role': 'user-role'  # from UserDetail
            })
            data = {
                'refresh': str(refresh),
                'access': str(refresh.access_token),  # Отправка на клиент
                'id': user.id,
                'username': user.username,
                'role': 'user-role'  # from UserDetail
            }
            status_code = status.HTTP_201_CREATED
        except Exception as e:
            data = {'success': False, 'error': str(e)}
            status_code = status.HTTP_200_OK

        response = Response(data=data, status=status_code)
        response.set_cookie(
            key='access_token',      # имя cookie
            value=str(refresh.access_token),  # значение (токен)
            httponly=True,           # недоступно из JS
            secure=True,             # только по HTTPS (рекомендуется)
            samesite='Lax',          # защита от CSRF
            max_age=SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'].total_seconds(),
            path='/'                 # путь
        )
        response.set_cookie(
            key='refresh_token',
            value=str(refresh),
            httponly=True,
            secure=True,
            samesite='Lax',
            max_age=SIMPLE_JWT['REFRESH_TOKEN_LIFETIME'].total_seconds(),
            path='/'
        )
        return response


class ObtainTokens(TokenObtainPairView):
    serializer_class = ObtainSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):

        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0]) from e

        user = User.objects.get(username=request.data.get('username'))
        data = {
            'success': True,
            'username': user.username,
            'role': 'user-role',
            'id': user.pk,
        }
        response = Response(data=data, status=status.HTTP_200_OK)
        # response = Response(serializer.validated_data, status=status.HTTP_200_OK)

        refresh = serializer.validated_data['refresh']
        access = serializer.validated_data['access']
        response.set_cookie(
            key='access_token',      # имя cookie
            value=str(access)+'1',       # значение (токен)
            httponly=True,           # недоступно из JS
            secure=True,             # только по HTTPS (рекомендуется)
            samesite='Lax',          # защита от CSRF
            max_age=SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'].total_seconds(),
            path='/'                 # путь
        )
        response.set_cookie(
            key='refresh_token',
            value=str(refresh),
            httponly=True,
            secure=True,
            samesite='Lax',
            max_age=SIMPLE_JWT['REFRESH_TOKEN_LIFETIME'].total_seconds(),
            path='/'
        )
        return response


class RefreshTokens(TokenRefreshView):
    serializer_class = TokenRefreshSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        # response = super().post(request, *args, **kwargs)

        serializer = self.get_serializer(
            data=request.data
        )
        # print(request.COOKIES.get('refresh_token'))

        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0]) from e

        # response = Response(serializer.validated_data, status=status.HTTP_200_OK)
        # response = Response(data={'success': True}, status=status.HTTP_200_OK)

        # refresh = serializer.validated_data['refresh']
        # access = serializer.validated_data['access']
        # response.set_cookie(
        #     key='access_token',      # имя cookie
        #     value=str(access),       # значение (токен)
        #     httponly=True,           # недоступно из JS
        #     secure=True,             # только по HTTPS (рекомендуется)
        #     samesite='Lax',          # защита от CSRF
        #     max_age=SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'].total_seconds(),
        #     path='/'                 # путь
        # )
        # response.set_cookie(
        #     key='refresh_token',
        #     value=str(refresh),
        #     httponly=True,
        #     secure=True,
        #     samesite='Lax',
        #     max_age=SIMPLE_JWT['REFRESH_TOKEN_LIFETIME'].total_seconds(),
        #     path='/'
        # )

        decoded_token = AccessToken(serializer.validated_data['access'])
        payload = decoded_token.payload
        data = {
            'is_valid': True,
            'id': payload['id'],
            'username': payload['username'],
            'role': payload['role'],
            'access': serializer.validated_data['access'],
            'refresh': serializer.validated_data['refresh'],
        }
        status_code = status.HTTP_200_OK

        return Response(data=data, status=status_code)


class VerifyToken(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):

        serializer = VerifySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # print(request.COOKIES.get('refresh_token'))
        # print(request.data)

        try:
            token = serializer.initial_data['token']
            decoded_token = AccessToken(token)
            payload = decoded_token.payload
            # user_id = decoded_token['user_id']  # from header (USER_ID_CLAIM)
            # print(payload)
            data = {
                'is_valid': True,
                'id': payload['id'],
                'username': payload['username'],
                'role': payload['role'],
            }
            status_code = status.HTTP_200_OK
        except TokenError:
            data = {'is_valid': False, 'error': 'Недействительный токен'}
            status_code = status.HTTP_400_BAD_REQUEST
        except Exception as e:
            data = {'is_valid': False, 'error': str(e)}
            status_code = status.HTTP_400_BAD_REQUEST

        return Response(data=data, status=status_code)


class AuthCheck(APIView):

    def get(self, request):

        tokens = {
            'access': request.COOKIES.get('access_token'),
            'refresh': request.COOKIES.get('refresh_token'),
        }
        is_correct = self.token_verification(tokens)

        if is_correct:
            return Response(
                data={'success': True, 'right': True},
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                data={'success': True, 'right': False},
                status=status.HTTP_200_OK,
            )

    def token_verification(self, tokens):
        is_correct = False
        if tokens['access']:
            is_correct = self.success_verification(tokens['access'])
            if is_correct:
                return True
        if tokens['refresh']:
            is_correct = self.refresh_verification(tokens['refresh'])

        return is_correct

    def success_verification(self, a_token):
        try:
            AccessToken(a_token)
            return True
        except TokenError:  # AccessToken вернул ошибку (токен неверный)
            return False

    def refresh_verification(self, r_token):
        try:
            RefreshToken(r_token)
            return True
        except TokenError:  # RefreshToken вернул ошибку (токен неверный)
            return False


class Logout(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        response = Response(
            data={'success': True},
            status=status.HTTP_200_OK
        )
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


class TestRequest(APIView):

    def get(self, request):
        print(request.COOKIES.get('refresh_token'))
        print(request.COOKIES.get('access_token'))
        print(request.data)
        request_data = {

        }
        return Response()
