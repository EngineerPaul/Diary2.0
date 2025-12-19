from rest_framework import serializers

from main.models import Note, Image


# ===== NoteAPI =====
class NoteGetSerializer(serializers.ModelSerializer):
    """Сериализатор для получения заметки (get)"""
    user_id = serializers.SerializerMethodField()

    class Meta:
        model = Note
        fields = ['pk', 'user_id', 'text', 'created_at', 'changed_at']
        read_only_fields = ['pk', 'created_at', 'changed_at']

    def get_user_id(self, obj):
        return obj.msg_id.record_id.user_id


# ===== NoteAPI =====
class NoteWriteSerializer(serializers.ModelSerializer):
    """Сериализатор для создания и обновления заметки (post/patch)"""

    class Meta:
        model = Note
        fields = ['text']


# ===== ImageAPI =====
class ImageGetSerializer(serializers.ModelSerializer):
    """Сериализатор для получения картинки (get)"""
    url = serializers.SerializerMethodField()

    class Meta:
        model = Image
        fields = ['pk', 'name', 'url']

    def get_url(self, obj):
        if not obj.file:
            raise serializers.ValidationError("Image file is missing")
        request = self.context.get('request')
        if request:
            return request.build_absolute_uri(obj.file.url)
        return obj.file.url


# ===== ImageAPI =====
class ImageCreateSerializer(serializers.ModelSerializer):
    """Сериализатор для добавления картинки в существующий message (post)"""

    class Meta:
        model = Image
        fields = ['file']

    def create(self, validated_data):
        user_id = self.context['user_id']
        message = self.context['message']
        file = validated_data['file']

        img = Image(msg_id=message, name=file.name, user_id=user_id)
        img.file.save(file.name, file, save=True)
        return img


# ===== ImagesAPI =====
class ImagesGetSerializer(serializers.ModelSerializer):
    """Сериализатор для получения блока картинок (get)"""
    url = serializers.SerializerMethodField()

    class Meta:
        model = Image
        fields = ['name', 'url']

    def get_url(self, obj):
        if not obj.file:
            raise serializers.ValidationError("Image file is missing")
        request = self.context.get('request')
        if request:
            return request.build_absolute_uri(obj.file.url)
        return obj.file.url


class ImagesCreateSerializer(serializers.ModelSerializer):
    """Сериализатор для создания нового блока картинок (post)"""

    class Meta:
        model = Image
        fields = ['file']

    def create(self, validated_data):
        user_id = self.context['user_id']
        message = self.context['message']
        file = validated_data['file']

        img = Image(msg_id=message, name=file.name, user_id=user_id)
        img.file.save(file.name, file, save=True)
        return img
