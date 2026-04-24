from django.contrib.auth import get_user_model
from django.db import models


USER = get_user_model()
class Reservation(models.Model):
    tabel = models.ForeignKey("table.Tabel", on_delete=models.CASCADE)
    user = models.ForeignKey(USER, on_delete=models.CASCADE)
    date = models.DateField()
    hour_start = models.IntegerField()
    hour_end = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
