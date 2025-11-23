from django.db import models


colors = [
    ('w', 'white'),
    ('g', 'green'),
    ('b', 'blue'),
    ('y', 'yellow'),
    ('r', 'red'),
]


class RecordFolder(models.Model):
    user_id = models.IntegerField()
    parent_id = models.ForeignKey('self', on_delete=models.SET_NULL,
                                  null=True, related_name='employees')
    title = models.CharField(max_length=20)
    color = models.CharField(max_length=1, choices=colors, default='w')
    nested_folders = models.TextField(null=False, blank=True, default='')
    nested_records = models.TextField(null=False, blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)
    changed_at = models.DateTimeField(auto_now=True)

    def add_folder(self, folder_id):
        if self.nested_folders == '':
            self.nested_folders = str(folder_id)
        else:
            self.nested_folders += f',{folder_id}'
        return True

    def insert_folder(self, folder_id, old_num, new_num):
        nested_list = self.nested_folders.split(',')
        nested_list.insert(new_num, str(folder_id))
        self.nested_folders = ','.join(nested_list)
        return True

    def del_folder(self, folder_id):
        try:
            nested_list = self.nested_folders.split(',')
            nested_list.remove(str(folder_id))
            self.nested_folders = ','.join(nested_list)
            return True
        except ValueError:
            return False

    def add_record(self, record_id):
        if self.nested_records == '':
            self.nested_records = str(record_id)
        else:
            self.nested_records += f',{record_id}'
        return True

    def insert_record(self, record_id, new_num):
        nested_list = self.nested_records.split(',')
        nested_list.insert(new_num, str(record_id))
        self.nested_records = ','.join(nested_list)
        return True

    def del_record(self, record_id):
        try:
            nested_list = self.nested_records.split(',')
            nested_list.remove(str(record_id))
            self.nested_records = ','.join(nested_list)
            return True
        except ValueError:
            return False


class Record(models.Model):
    user_id = models.IntegerField()
    folder_id = models.ForeignKey(RecordFolder, on_delete=models.CASCADE, related_name='records')
    title = models.CharField(max_length=20)
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
    # created_at = models.DateTimeField(auto_now_add=True)
    # changed_at = models.DateTimeField(auto_now=True)


class Image(models.Model):
    msg_id = models.ForeignKey(
        Message, on_delete=models.CASCADE, related_name='images')
    url = models.CharField(max_length=100)
    # created_at = models.DateTimeField(auto_now_add=True)
    # changed_at = models.DateTimeField(auto_now=True)
    # url = models.FileField()
