
from django.db import models
from django.db.models import ManyToManyField
from django.db.models.signals import post_save
from django.dispatch import receiver


class Feature(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name

class Favorites(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey('authentication.User', on_delete=models.CASCADE)
    table = models.ForeignKey("Table", on_delete=models.CASCADE)
    class Meta:
        unique_together = ('user', 'table')





class Table(models.Model):
    number = models.IntegerField()
    image = models.ImageField(upload_to='table_image/')
    seats = models.IntegerField()
    description = models.TextField()
    feature = ManyToManyField("Feature", blank=True)


    def __str__(self):
        return str(self.number)


@receiver(post_save,sender=Table)
def post_save_table(sender, instance, created, **kwargs):
    from .tasks import email_sender
    if created:
        email_sender.delay(instance.id)






