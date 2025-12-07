from rest_framework import serializers

from main.models import UploadedTest


class UploadTestSerializer(serializers.ModelSerializer):

    class Meta:
        model = UploadedTest
        fields = ['id', 'title', 'file', 'user_id']
        read_only_fields = ['id']

    def validate_file(self, value):

        if value.size > 5*1024*1024:  # 5 МБайт
            msg = "Максимальный размер файла - 5 МБайт"
            raise serializers.ValidationError(msg)

        allowed_types = ['image/jpeg', 'image/png', 'image/webp']
        if value.content_type not in allowed_types:
            msg = "Неверный формат данных"
            raise serializers.ValidationError(msg)
        return value
