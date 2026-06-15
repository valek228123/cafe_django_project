import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import ForeignKey
from django.views import View


class User(AbstractUser):
    favorites_tables = models.ManyToManyField("table.Table", through="table.Favorites", blank=True,related_name='favorited_by')



class PasswordResetToken(models.Model):
    user = ForeignKey(User, related_name='password_reset_token', on_delete=models.CASCADE)
    token = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.token}"

