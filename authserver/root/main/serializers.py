import re
from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .models import UserDetails


class CredentialSerializer(serializers.Serializer):
    username = serializers.CharField(
        max_length=15,
        min_length=6,
        required=True,
        allow_blank=False
    )
    password = serializers.CharField(
        max_length=20,
        min_length=6,
        required=True,
        allow_blank=False
    )

    def validate_username(self, value):
        if re.search(r'[^a-zA-Z0-9]', value):
            raise serializers.ValidationError(
                'Поле содержит недопустимые символы.'
            )
        return value

    def validate_password(self, value):
        if re.search(r'[^a-zA-Z0-9]', value):
            raise serializers.ValidationError(
                'Поле содержит недопустимые символы.'
            )
        return value


class RegSerializer(CredentialSerializer):

    def create(self, validated_data):
        user = User(
            username=validated_data['username']
        )
        user.set_password(validated_data['password'])
        user.save()

        # добавить UserDetail
        return user


class VerifySerializer(serializers.Serializer):
    token = serializers.CharField(write_only=True)


class ObtainSerializer(CredentialSerializer, TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # token['user_id'] = user.pk
        token['id'] = user.pk
        token['username'] = user.username
        token['role'] = 'user-role'
        return token


class TelegramActivationSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = UserDetails
        fields = ['chat_id', 'tg_user_id', 'tg_username']
        extra_kwargs = {
            'chat_id': {'write_only': True},
            'tg_user_id': {'write_only': True},
            'tg_username': {'write_only': True},
        }


class GetChatIdsSerializer(serializers.Serializer):
    user_ids = serializers.ListField(child=serializers.IntegerField())


class GetUserIdSerializer(serializers.Serializer):
    chat_id = serializers.IntegerField(write_only=True)
