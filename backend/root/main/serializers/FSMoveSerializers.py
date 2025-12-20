from rest_framework import serializers


class MoveBetweenSerializer(serializers.Serializer):
    """Сериализатор для изменения порядка объекта внутри папки"""

    type = serializers.CharField()
    object_id = serializers.IntegerField(min_value=1)
    folder_id = serializers.IntegerField(min_value=1)
    nested_list = serializers.ListField(
        child=serializers.IntegerField(min_value=1))

    def validate_type(self, value):
        allowed_values = ['record', 'recordFolder', 'notice', 'noticeFolder']
        if value not in allowed_values:
            msg = f'Допустимые значения {", ".join(allowed_values)}'
            raise serializers.ValidationError(msg)
        return value


class MoveInsideSerializer(serializers.Serializer):
    """Сериализатор для перемещения объекта внутрь папки"""

    type = serializers.CharField()
    object_id = serializers.IntegerField(min_value=1)
    old_folder_id = serializers.IntegerField(min_value=1)
    new_folder_id = serializers.IntegerField(min_value=1)

    def validate_type(self, value):
        allowed_values = ['record', 'recordFolder', 'notice', 'noticeFolder']
        if value not in allowed_values:
            msg = f'Допустимые значения {", ".join(allowed_values)}'
            raise serializers.ValidationError(msg)
        return value
