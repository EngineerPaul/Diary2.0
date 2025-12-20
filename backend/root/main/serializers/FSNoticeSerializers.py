from rest_framework import serializers

from main.models import NoticeFolder, Notice
from .utils import ChildrenMixin


# ===== NoticesFSAPI =====
class NoticeFolderFSSerializer(ChildrenMixin, serializers.ModelSerializer):
    """Сериализатор папки для файловой системы (get only)"""
    children = serializers.SerializerMethodField()  # ChildrenMixin

    class Meta:
        model = NoticeFolder
        fields = [
            'pk', 'parent_id', 'title', 'color', 'changed_at', 'children'
        ]


# ===== NoticesFSAPI =====
class NoticeFSSerializer(serializers.ModelSerializer):
    """Сериализатор записи для файловой системы (get only)"""

    class Meta:
        model = Notice
        fields = [
            'pk', 'folder_id', 'title', 'description', 'color',
            'changed_at', 'next_date', 'time'
        ]


# ===== NoticesAPI =====
class NoticeGetSerializer(serializers.ModelSerializer):
    """NoticesAPI Сериализатор для получения записи (get)"""

    class Meta:
        model = Notice
        fields = [
            'pk', 'folder_id', 'title', 'description', 'color',
            'changed_at', 'next_date', 'time', 'period'
        ]


# ===== NoticesAPI =====
class NoticeCreateSerializer(serializers.ModelSerializer):
    """NoticesAPI Сериализатор для создания записи (post)"""

    initial_date = serializers.DateField(required=False, write_only=True)

    class Meta:
        model = Notice
        fields = [
            'pk', 'folder_id', 'title', 'description', 'color',
            'changed_at', 'next_date', 'time', 'period', 'initial_date'
        ]
        read_only_fields = ['pk', 'changed_at', 'next_date']

    def save(self, **kwargs):
        self.validated_data.pop('initial_date', None)
        return super().save(**kwargs)


# ===== NoticesAPI =====
class NoticeUpdateSerializer(serializers.ModelSerializer):
    """NoticesAPI Сериализатор для обновления записи (patch)"""

    initial_date = serializers.DateField(required=False, write_only=True)

    class Meta:
        model = Notice
        fields = [
            'pk', 'title', 'description', 'color', 'changed_at',
            'next_date', 'time', 'period', 'initial_date'
        ]
        read_only_fields = ['pk', 'changed_at', 'next_date']
        extra_kwargs = {
            'title': {'required': False},
            'description': {'required': False},
            'color': {'required': False},
            'time': {'required': False},
            'period': {'required': False},
        }

    def save(self, **kwargs):
        self.validated_data.pop('initial_date', None)
        return super().save(**kwargs)


# ===== NoticeFoldersAPI =====
class FolderGetSerializer(ChildrenMixin, serializers.ModelSerializer):
    """Сериализатор для получения папки (get)"""
    children = serializers.SerializerMethodField()  # ChildrenMixin

    class Meta:
        model = NoticeFolder
        fields = [
            'pk', 'parent_id', 'title', 'color', 'changed_at', 'children'
        ]


# ===== NoticeFoldersAPI =====
class FolderCreateSerializer(serializers.ModelSerializer):
    """Сериализатор для создания папки (post)"""

    class Meta:
        model = NoticeFolder
        fields = ['pk', 'parent_id', 'title', 'color', 'changed_at']
        read_only_fields = ['pk', 'changed_at']


# ===== NoticeFoldersAPI =====
class FolderUpdateSerializer(serializers.ModelSerializer):
    """Сериализатор для обновления папки (patch)"""

    class Meta:
        model = NoticeFolder
        fields = ['pk', 'title', 'color', 'changed_at']
        read_only_fields = ['pk', 'changed_at']
        extra_kwargs = {
            'title': {'required': False},
            'color': {'required': False},
        }
