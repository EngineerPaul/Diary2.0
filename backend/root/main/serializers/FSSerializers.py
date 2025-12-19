from rest_framework import serializers

from main.models import RecordFolder, Record


class ChildrenMixin:
    """Миксин для формирования children из nested_folders и nested_objects"""

    def get_children(self, obj):
        nested_folders = []
        nested_objects = []
        if obj.nested_folders:
            nested_folders = [f'f{f_id}' for f_id in obj.nested_folders.split(',')]
        if obj.nested_objects:
            nested_objects = [f'n{r_id}' for r_id in obj.nested_objects.split(',')]
        return ','.join(nested_folders + nested_objects)


# ===== RecordsFSAPI =====
class RecordFolderFSSerializer(ChildrenMixin, serializers.ModelSerializer):
    """Сериализатор папки для файловой системы (get only)"""
    children = serializers.SerializerMethodField()  # ChildrenMixin

    class Meta:
        model = RecordFolder
        fields = ['pk', 'parent_id', 'title', 'color', 'changed_at', 'children']


# ===== RecordsFSAPI =====
class RecordFSSerializer(serializers.ModelSerializer):
    """Сериализатор записи для файловой системы (get only)"""

    class Meta:
        model = Record
        fields = ['pk', 'folder_id', 'title', 'description', 'color', 'changed_at']


# ===== RecordsAPI =====
class RecordGetSerializer(serializers.ModelSerializer):
    """RecordsAPI Сериализатор для получения записи (get)"""

    class Meta:
        model = Record
        fields = ['pk', 'folder_id', 'title', 'description', 'color', 'changed_at']


# ===== RecordsAPI =====
class RecordCreateSerializer(serializers.ModelSerializer):
    """RecordsAPI Сериализатор для создания записи (post)"""

    class Meta:
        model = Record
        fields = ['pk', 'folder_id', 'title', 'description', 'color', 'changed_at']
        read_only_fields = ['pk', 'changed_at']


# ===== RecordsAPI =====
class RecordUpdateSerializer(serializers.ModelSerializer):
    """RecordsAPI Сериализатор для обновления записи (patch)"""

    class Meta:
        model = Record
        fields = ['pk', 'title', 'description', 'color', 'changed_at']
        read_only_fields = ['pk', 'changed_at']
        extra_kwargs = {
            'title': {'required': False},
            'color': {'required': False},
        }


# ===== RecordFoldersAPI =====
class FolderGetSerializer(ChildrenMixin, serializers.ModelSerializer):
    """Сериализатор для получения папки (get)"""
    children = serializers.SerializerMethodField()  # ChildrenMixin

    class Meta:
        model = RecordFolder
        fields = ['pk', 'parent_id', 'title', 'color', 'changed_at', 'children']


# ===== RecordFoldersAPI =====
class FolderCreateSerializer(serializers.ModelSerializer):
    """Сериализатор для создания папки (post)"""

    class Meta:
        model = RecordFolder
        fields = ['pk', 'parent_id', 'title', 'color', 'changed_at']
        read_only_fields = ['pk', 'changed_at']


# ===== RecordFoldersAPI =====
class FolderUpdateSerializer(serializers.ModelSerializer):
    """Сериализатор для обновления папки (patch)"""

    class Meta:
        model = RecordFolder
        fields = ['pk', 'title', 'color', 'changed_at']
        read_only_fields = ['pk', 'changed_at']
        extra_kwargs = {
            'title': {'required': False},
            'color': {'required': False},
        }


# ===== MoveAPI =====
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


# ===== MoveAPI =====
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
