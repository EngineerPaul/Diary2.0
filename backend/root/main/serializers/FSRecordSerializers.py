from rest_framework import serializers

from main.models import RecordFolder, Record
from .utils import ChildrenMixin


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
