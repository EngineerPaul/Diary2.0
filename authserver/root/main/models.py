from django.db import models
from django.contrib.auth.models import User


class UserDetails(models.Model):
    """ Additional (telegram) user data """
    user_id = models.OneToOneField(User, on_delete=models.CASCADE)
    tg_user_id = models.IntegerField(null=True)
    tg_username = models.CharField(max_length=32, null=True)
    chat_id = models.IntegerField(null=True)
    tg_activation_date = models.DateTimeField(null=True)

    def __str__(self):
        return self.user_id.username
