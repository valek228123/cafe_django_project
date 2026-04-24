from django.db import models

class Tabel(models.Model):
    number = models.IntegerField()
    image = models.ImageField(upload_to='table_image/')
    seats = models.IntegerField()
    description = models.TextField()
    is_free = models.BooleanField(default=True)

    class Meta:
        db_table = 'tabel_tabel'


# Create your models here.

