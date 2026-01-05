from rest_framework import serializers

from main.models import Note, Image, NoticeImage


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

    def validate_file(self, value):
        """Валидация размера файла"""
        max_size = 5 * 1024 * 1024  # 5 МБ
        if value.size > max_size:
            max_mb = max_size // (1024 * 1024)
            raise serializers.ValidationError(
                f'Размер файла не должен превышать {max_mb} МБ'
            )
        return value


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

    def validate_file(self, value):
        """Валидация размера файла"""
        max_size = 5 * 1024 * 1024  # 5 МБ
        if value.size > max_size:
            max_mb = max_size // (1024 * 1024)
            raise serializers.ValidationError(
                f'Размер файла не должен превышать {max_mb} МБ'
            )
        return value


class ImageNoticeCreateSerializer(serializers.ModelSerializer):
    """Сериализатор для добавления картинок в напоминание (post)"""

    class Meta:
        model = NoticeImage
        fields = ['file']

    def validate_file(self, value):
        """Валидация размера файла"""
        max_size = 5 * 1024 * 1024  # 5 МБ
        if value.size > max_size:
            max_mb = max_size // (1024 * 1024)
            raise serializers.ValidationError(
                f'Размер файла не должен превышать {max_mb} МБ'
            )
        return value

    def create(self, validated_data):
        user_id = self.context['user_id']
        notice = self.context['notice']
        file = validated_data['file']

        img = NoticeImage(notice=notice, name=file.name, user_id=user_id)
        img.file.save(file.name, file, save=True)
        return img


class ImageNoticeGetSerializer(serializers.ModelSerializer):
    """Сериализатор для получения картинок напоминания (get)"""

    url = serializers.SerializerMethodField()
    image_id = serializers.IntegerField(source='pk', read_only=True)

    class Meta:
        model = NoticeImage
        fields = ['image_id', 'name', 'url']

    def get_url(self, obj):
        if not obj.file:
            raise serializers.ValidationError("Image file is missing")
        request = self.context.get('request')
        if request:
            return request.build_absolute_uri(obj.file.url)
        return obj.file.url
