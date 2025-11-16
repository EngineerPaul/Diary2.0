from django.db import models


class Record(models.Model):
    user_id = models.IntegerField()
    title = models.CharField(max_length=20)


class Message(models.Model):
    record_id = models.ForeignKey(
        Record, on_delete=models.CASCADE, related_name='messages')


class Note(models.Model):
    msg_id = models.ForeignKey(
        Message, on_delete=models.CASCADE, related_name='notes')
    text = models.TextField()
    # created_at = models.DateTimeField(auto_now_add=True)
    # changed_at = models.DateTimeField(auto_now=True)


class Image(models.Model):
    msg_id = models.ForeignKey(
        Message, on_delete=models.CASCADE, related_name='images')
    url = models.CharField(max_length=100)
    # url = models.FileField()
    # created_at = models.DateTimeField(auto_now_add=True)
