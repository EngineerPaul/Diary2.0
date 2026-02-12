from datetime import timedelta

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework.permissions import AllowAny
from django.contrib.auth.models import User
from django.db.models import F
from django.utils import timezone
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from rest_framework_simplejwt.exceptions import InvalidToken
from django.conf import settings
from .models import UserDetails

from .serializers import (
    RegSerializer,
    VerifySerializer,
    ObtainSerializer,
    TelegramActivationSerializer,
    GetChatIdsSerializer,
    GetUserIdSerializer,
)
from .queries import create_root_folders
from root.settings import TGAuthTimeout, SSL


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
            user, timezone_value = serializer.save()
            user_details = UserDetails.objects.create(
                user_id=user,
                tg_user_id=None,
                chat_id=None,
                tg_activation_date=timezone.now(),
                timezone=timezone_value
            )

            # Create root folders on backend server
            create_root_folders(user.id)

            refresh = RefreshToken.for_user(user)  # Создание Refesh и Access
            refresh.payload.update({  # Полезная информация в самом токене
                'id': user.id,
                'username': user.username,
                'role': 'user-role',  # from UserDetails
                'timezone': user_details.timezone
            })
            data = {
                'refresh': str(refresh),
                'access': str(refresh.access_token),  # Отправка на клиент
                'id': user.id,
                'username': user.username,
                'role': 'user-role',  # from UserDetails
                'timezone': user_details.timezone
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
            secure=SSL,              # только по HTTPS (рекомендуется)
            samesite='Lax',          # защита от CSRF
            max_age=settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'].total_seconds(),
            path='/'                 # путь
        )
        response.set_cookie(
            key='refresh_token',
            value=str(refresh),
            httponly=True,
            secure=SSL,
            samesite='Lax',
            max_age=settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME'].total_seconds(),
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
            return Response(e, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.select_related('userdetails').get(
                username=request.data.get('username')
            )
        except User.DoesNotExist:
            return Response(
                {'success': False, 'error': 'User not found'},
                status=status.HTTP_404_NOT_FOUND
            )

        try:
            tg_nickname = user.userdetails.tg_username
        except UserDetails.DoesNotExist:
            tg_nickname = None
        user_timezone = user.userdetails.timezone

        data = {
            'success': True,
            'username': user.username,
            'role': 'user-role',
            'id': user.pk,
            'tg_nickname': tg_nickname,
            'timezone': user_timezone,
        }
        response = Response(data=data, status=status.HTTP_200_OK)
        # response = Response(serializer.validated_data, status=status.HTTP_200_OK)

        refresh = serializer.validated_data['refresh']
        access = serializer.validated_data['access']
        response.set_cookie(
            key='access_token',      # имя cookie
            value=str(access),       # значение (токен)
            httponly=True,           # недоступно из JS
            secure=SSL,              # только по HTTPS (рекомендуется)
            samesite='Lax',          # защита от CSRF
            max_age=settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'].total_seconds(),
            path='/'                 # путь
        )
        response.set_cookie(
            key='refresh_token',
            value=str(refresh),
            httponly=True,
            secure=SSL,
            samesite='Lax',
            max_age=settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME'].total_seconds(),
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

        try:
            serializer.is_valid(raise_exception=True)
        except ValidationError as e:
            return Response(
                {'is_valid': False, 'error': f'Ошибка валидации: {e}',
                 'details': e.detail},
                status=status.HTTP_400_BAD_REQUEST
            )
        except TokenError as e:
            return Response(
                {'is_valid': False, 'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response(
                {'is_valid': False, 'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

        # response = Response(serializer.validated_data, status=status.HTTP_200_OK)
        # response = Response(data={'success': True}, status=status.HTTP_200_OK)

        # refresh = serializer.validated_data['refresh']
        # access = serializer.validated_data['access']
        # response.set_cookie(
        #     key='access_token',      # имя cookie
        #     value=str(access),       # значение (токен)
        #     httponly=True,           # недоступно из JS
        #     secure=SSL,              # только по HTTPS (рекомендуется)
        #     samesite='Lax',          # защита от CSRF
        #     max_age=settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'].total_seconds(),
        #     path='/'                 # путь
        # )
        # response.set_cookie(
        #     key='refresh_token',
        #     value=str(refresh),
        #     httponly=True,
        #     secure=SSL,
        #     samesite='Lax',
        #     max_age=settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME'].total_seconds(),
        #     path='/'
        # )

        decoded_token = AccessToken(serializer.validated_data['access'])
        payload = decoded_token.payload
        data = {
            'is_valid': True,
            'id': payload['id'],
            'username': payload['username'],
            'role': payload['role'],
            'timezone': payload['timezone'],
            'access': serializer.validated_data['access'],
            'refresh': serializer.validated_data['refresh'],
        }
        status_code = status.HTTP_200_OK

        return Response(data=data, status=status_code)


class VerifyToken(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):

        serializer = VerifySerializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except ValidationError as e:
            return Response(
                {'is_valid': False, 'error': f'Ошибка валидации: {e}',
                 'details': e.detail},
                status=status.HTTP_400_BAD_REQUEST
            )

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
                'timezone': payload['timezone'],
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


# ======== Telegram API ========
class TGAuthDate(APIView):
    """ Запечатление даты перехода по ссылке при запуске Telegram бота """
    permission_classes = [AllowAny]

    def post(self, request):

        access_token = request.COOKIES.get('access_token')
        refresh_token = request.COOKIES.get('refresh_token')

        if access_token:
            try:
                decoded_token = AccessToken(access_token)
                payload = decoded_token.payload

                # data = {
                #     'is_valid': True,
                #     'id': payload['user_id'],
                #     'username': payload.get('username', ''),
                #     'role': payload.get('role', 'user'),
                # }
                user_id = int(payload['user_id'])
            except TokenError:
                return Response(
                    {'success': False, 'is_valid': False, 'error': 'Invalid access token'},
                    status=status.HTTP_401_UNAUTHORIZED
                )

        elif refresh_token:
            try:
                refresh = RefreshToken(refresh_token)
                new_access = str(refresh.access_token)
                new_refresh = str(refresh.refresh_token)

                decoded_token = AccessToken(new_access)
                payload = decoded_token.payload

                response = Response(status=status.HTTP_200_OK)
                response.set_cookie(
                    'access_token', new_access,
                    max_age=settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'],
                    httponly=True,
                    samesite='Lax',
                    path='/'
                )
                response.set_cookie(
                    'refresh_token', new_refresh,
                    max_age=settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME'],
                    httponly=True,
                    samesite='Lax',
                    path='/'
                )
                user_id = int(payload['user_id'])

            except TokenError:
                return Response(
                    {'success': False, 'is_valid': False,
                     'error': 'Invalid refresh token'},
                    status=status.HTTP_401_UNAUTHORIZED
                )

        else:  # Нет токенов
            return Response(
                {'success': False, 'is_valid': False,
                 'error': 'No valid tokens provided'},
                status=status.HTTP_401_UNAUTHORIZED
            )

        user = User.objects.select_related('userdetails').get(id=user_id)
        try:
            user.userdetails.tg_activation_date = timezone.now()
            user.userdetails.save()
        except UserDetails.DoesNotExist:
            UserDetails.objects.create(
                user_id=user,
                tg_user_id=None,
                chat_id=None,
                tg_activation_date=timezone.now(),
                timezone='UTC'
            )
        return Response(
            {'success': True},
            status=status.HTTP_200_OK
        )


class TGAuthCheck(APIView):
    """ Frontend check tg nickname """

    def get(self, request):

        access_token = request.COOKIES.get('access_token')
        refresh_token = request.COOKIES.get('refresh_token')

        if access_token:
            try:
                decoded_token = AccessToken(access_token)
                payload = decoded_token.payload
                user_id = int(payload['user_id'])
            except TokenError:
                return Response(
                    {'success': False, 'is_valid': False, 'error': 'Invalid access token'},
                    status=status.HTTP_401_UNAUTHORIZED
                )
        elif refresh_token:
            try:
                refresh = RefreshToken(refresh_token)
                new_access = str(refresh.access_token)
                new_refresh = str(refresh.refresh_token)
                decoded_token = AccessToken(new_access)
                payload = decoded_token.payload

                response = Response(status=status.HTTP_200_OK)
                response.set_cookie(
                    'access_token', new_access,
                    max_age=settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'],
                    httponly=True,
                    samesite='Lax',
                    path='/'
                )
                response.set_cookie(
                    'refresh_token', new_refresh,
                    max_age=settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME'],
                    httponly=True,
                    samesite='Lax',
                    path='/'
                )
                user_id = int(payload['user_id'])
            except TokenError:
                return Response(
                    {'success': False, 'is_valid': False,
                     'error': 'Invalid refresh token'},
                    status=status.HTTP_401_UNAUTHORIZED
                )

        else:  # Нет токенов
            return Response(
                {'success': False, 'is_valid': False,
                 'error': 'No valid tokens provided'},
                status=status.HTTP_401_UNAUTHORIZED
            )

        user = User.objects.select_related('userdetails').get(pk=user_id)

        data = {
            'user_id': user.pk,
            'tg_nickname': user.userdetails.tg_username
        }
        return Response(data=data, status=status.HTTP_200_OK)


class TGAuthDetails(APIView):
    """ Сохранение данных Telegram бота """
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = TelegramActivationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user_id = serializer.validated_data['user_id']

        user = User.objects.select_related('userdetails').get(id=user_id)

        # Создаем сериализатор с instance для обновления существующего объекта
        serializer = TelegramActivationSerializer(
            instance=user.userdetails,
            data=request.data,
            partial=True
        )
        serializer.is_valid(raise_exception=True)

        try:
            if user.userdetails.tg_activation_date is None:
                return Response(
                    {'success': False, 'is_valid': False,
                     'error': 'Activation date is None'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            if timezone.now() - user.userdetails.tg_activation_date > timedelta(
                seconds=TGAuthTimeout
            ):
                return Response(
                    {'success': False, 'is_valid': False,
                     'error': 'Activation timeout'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            serializer.save(
                user=user,
                tg_activation_date=None
            )

        except UserDetails.DoesNotExist:
            return Response(
                {'success': False, 'is_valid': False,
                 'error': 'UserDetails not found'},
                status=status.HTTP_400_BAD_REQUEST
            )

        return Response({'success': True}, status=status.HTTP_200_OK)


class GetChatIds(APIView):
    """ Получение chat_id по списку user_id (pk) """
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = GetChatIdsSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user_ids = serializer.validated_data['user_ids']
        users = User.objects.select_related('userdetails').filter(
            id__in=user_ids).annotate(
            user_id=F('id'),
            chat_id=F('userdetails__chat_id')
        ).values('user_id', 'chat_id')
        return Response(
            {'success': True, 'data': users},
            status=status.HTTP_200_OK
        )


class GetUserId(APIView):
    """ Возвращает user_id (pk) по chat_id """
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = GetUserIdSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        chat_id = serializer.validated_data['chat_id']
        user = User.objects.select_related('userdetails').filter(
            userdetails__chat_id=chat_id).last()
        if not user:
            return Response(
                {'success': False, 'error': 'User not found'},
                status=status.HTTP_400_BAD_REQUEST
            )
        return Response(
            {'success': True, 'user_id': user.id},
            status=status.HTTP_200_OK
        )


class TestRequest(APIView):

    def get(self, request):
        print(request.COOKIES.get('refresh_token'))
        print(request.COOKIES.get('access_token'))
        print(request.data)
        return Response()
