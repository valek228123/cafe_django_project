from django.db import models
from django.db.models import ManyToManyField

class Feature(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name


class Table(models.Model):
    number = models.IntegerField()
    image = models.ImageField(upload_to='table_image/')
    seats = models.IntegerField()
    description = models.TextField()
    feature = ManyToManyField("Feature", blank=True)

    def __str__(self):
        return str(self.number)








