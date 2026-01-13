from rest_framework import serializers


class NewNoticeSerializer(serializers.Serializer):
    """ Сериализатор для создания нового напоминания """
    username = serializers.CharField(max_length=33, min_length=6)
    title = serializers.CharField(max_length=100)
    date = serializers.DateTimeField()
    chat_id = serializers.IntegerField()


class NoticeShiftSerializer(serializers.Serializer):
    """ Сериализатор для смещения напоминания на час/день """
    user_id = serializers.IntegerField(min_value=1)
    reminder_id = serializers.IntegerField(min_value=1)
    mode = serializers.ChoiceField(choices=['hour', 'day'])
    chat_id = serializers.IntegerField()


class UserInfoSerializer(serializers.Serializer):
    """ Сериализатор для сохранения информации о пользователе """
    tg_user_id = serializers.IntegerField()
    chat_id = serializers.IntegerField()
