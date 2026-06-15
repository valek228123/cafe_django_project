from celery import shared_task

from django.conf import settings
from .models import Table
from authentication.models import User
from django.core.mail import send_mail

@shared_task
def email_sender(table_id : int) -> None:
    table = Table.objects.get(id=table_id)
    subject = "В нашем ресторане обнавления!!!!"
    text = (f"Появился новый стол номер {table.number}!"
            f"Количество мест {table.seats}."
            f"{table.description}."
            f"Вы можеет опробывать его уже сейчас")
    print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!1",[user.email for user in User.objects.all()])
    users_emails = [user.email for user in User.objects.all() if user.email != ""]
    send_mail(subject, text, settings.EMAIL_HOST_USER, users_emails)
    print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!2",users_emails)

