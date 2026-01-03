from datetime import datetime
import re
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
            'changed_at', 'next_date', 'time', 'period'
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
        # self.validated_data['next_date'] = date.today()
        return super().save(**kwargs)

    def validate_period(self, value):
        re_pattern = r'^\d+,\d+,\d+,\d+$'
        if not re.match(re_pattern, value):
            msg = 'Validate error: period pattern is incorrect'
            raise serializers.ValidationError(msg)
        return value

    def validate(self, attrs):
        # validation of initial_date & time
        initial_date = attrs.get('initial_date')
        time_value = attrs.get('time')
        if initial_date and time_value:
            initial_datetime = datetime.combine(initial_date, time_value)
            now = datetime.now()
            if initial_datetime <= now:
                msg = ('Validate error: initial_date and time together must '
                       'be greater than current datetime')
                raise serializers.ValidationError(msg)

        return attrs


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

    def validate_period(self, value):
        re_pattern = r'^\d+,\d+,\d+,\d+$'
        if not re.match(re_pattern, value):
            msg = 'Validate error: period pattern is incorrect'
            raise serializers.ValidationError(msg)
        return value

    def validate(self, attrs):
        # validation of initial_date & time
        initial_date = attrs.get('initial_date')
        time_value = attrs.get('time')
        if initial_date and time_value:
            initial_datetime = datetime.combine(initial_date, time_value)
            now = datetime.now()
            if initial_datetime <= now:
                msg = ('Validate error: initial_date and time together must '
                       'be greater than current datetime')
                raise serializers.ValidationError(msg)

        return attrs


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
