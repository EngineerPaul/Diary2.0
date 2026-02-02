from django.db import models
import uuid
import os
from datetime import datetime
from functools import partial


colors = [
    ('w', 'white'),
    ('g', 'green'),
    ('b', 'blue'),
    ('y', 'yellow'),
    ('r', 'red'),
]


class BaseFolder (models.Model):
    user_id = models.IntegerField()
    title = models.CharField(max_length=20)
    color = models.CharField(max_length=1, choices=colors, default='w')
    nested_folders = models.TextField(null=False, blank=True, default='')
    nested_objects = models.TextField(null=False, blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)
    changed_at = models.DateTimeField(auto_now=True)

    def add_folder(self, folder_id):
        if self.nested_folders == '':
            self.nested_folders = str(folder_id)
        else:
            self.nested_folders += f',{folder_id}'
        return True

    def del_folder(self, folder_id):
        try:
            nested_list = self.nested_folders.split(',')
            nested_list.remove(str(folder_id))
            self.nested_folders = ','.join(nested_list)
            return True
        except ValueError:
            return False

    def add_object(self, record_id):
        if self.nested_objects == '':
            self.nested_objects = str(record_id)
        else:
            self.nested_objects += f',{record_id}'
        return True

    def del_object(self, record_id):
        try:
            nested_list = self.nested_objects.split(',')
            nested_list.remove(str(record_id))
            self.nested_objects = ','.join(nested_list)
            return True
        except ValueError:
            return False

    class Meta:
        abstract = True


class RecordFolder(BaseFolder):
    parent_id = models.ForeignKey('self', on_delete=models.CASCADE,
                                  null=True, related_name='folders')


class NoticeFolder(BaseFolder):
    parent_id = models.ForeignKey('self', on_delete=models.CASCADE,
                                  null=True, related_name='folders')


class Record(models.Model):
    user_id = models.IntegerField()
    folder_id = models.ForeignKey(
        RecordFolder, on_delete=models.CASCADE, related_name='records')
    description = models.TextField(null=True, blank=True)
    title = models.CharField(max_length=50)
    color = models.CharField(max_length=1, choices=colors, default='w')
    created_at = models.DateTimeField(auto_now_add=True)
    changed_at = models.DateTimeField(auto_now=True)


class Message(models.Model):
    record_id = models.ForeignKey(
        Record, on_delete=models.CASCADE, related_name='messages')


class Note(models.Model):
    msg_id = models.ForeignKey(
        Message, on_delete=models.CASCADE, related_name='notes')
    text = models.TextField(max_length=10_000)
    created_at = models.DateTimeField(auto_now_add=True)
    changed_at = models.DateTimeField(auto_now=True)


def get_unique_path(instance, filename, subfolder):
    """ Создание уникального пути для сохранения файлов.
    Файлы заметок и напоминаний сохраняются в разные папки,
    указанные в классах картинок как subfolder """

    ext = os.path.splitext(filename)[1].lower()
    unique_name = f'{uuid.uuid4().hex}{ext}'
    date = datetime.now()
    date = f'{date.month}.{date.year}'
    user_id = instance.user_id
    path = os.path.join("uploads", subfolder, f"user_{user_id}",
                        date, unique_name)
    return path


class Image(models.Model):
    msg_id = models.ForeignKey(
        Message, on_delete=models.CASCADE, related_name='images')
    name = models.CharField(max_length=63)
    file = models.ImageField(
        upload_to=partial(get_unique_path, subfolder="records")
    )
    user_id = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)


class Notice(models.Model):
    user_id = models.IntegerField()
    folder_id = models.ForeignKey(
        NoticeFolder, on_delete=models.CASCADE, related_name='notices')
    description = models.TextField(null=True, blank=True)
    title = models.CharField(max_length=50)
    color = models.CharField(max_length=1, choices=colors, default='w')
    created_at = models.DateTimeField(auto_now_add=True)
    changed_at = models.DateTimeField(auto_now=True)
    next_date = models.DateField()
    time = models.TimeField()
    period = models.CharField(max_length=9, null=True, blank=True)
    # period is field like "0,0,0,0". Here the day, week, month, year are given
    # reading should be from right to left
    # the rightmost one set periodicity. Others indicate the certain date


class NoticeImage(models.Model):
    notice = models.ForeignKey(Notice, on_delete=models.CASCADE,
                               related_name='images')
    name = models.CharField(max_length=63)
    file = models.ImageField(
        upload_to=partial(get_unique_path, subfolder="notices")
    )
    user_id = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
