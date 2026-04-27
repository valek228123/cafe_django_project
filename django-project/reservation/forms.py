from django import forms
from django.core.exceptions import ValidationError
from reservation.models import Reservation
from datetime import datetime


class ReservationForm(forms.ModelForm):
    class Meta:

        model = Reservation
        fields = ['date', 'hour_start', 'hour_end']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'hour_start': forms.NumberInput(attrs={'placeholder': 'Например 12', 'min': '8', 'max': '18'}),
            'hour_end': forms.NumberInput(attrs={'placeholder': 'Например 12', 'min': '8', 'max': '18'}),
        }

        labels = {
            'date': 'Дата бронирования',
            'hour_start': 'Время начала бронирования',
            'hour_end': 'Время конца бронирования',
        }

    def clean(self):
        cleaned_data = super().clean()
        hour_start = cleaned_data.get('hour_start')
        hour_end = cleaned_data.get('hour_end')
        date = cleaned_data.get('date')
        date_now = datetime.now()
        all_reservations = Reservation.objects.filter(date = date)
        if hour_start and hour_end:
            if hour_start >= hour_end:
                raise ValidationError("Время начала должно быть раньше времени конца!")
        if date_now.date() > date:
            raise ValidationError("Выберите корректную дату")
        if hour_start  < date_now.hour + 1 and date_now.date() == date:
            raise ValidationError("Выберите корректное время")
        for reservation in all_reservations:
            if (hour_start < reservation.hour_start and hour_end <= reservation.hour_start) or (hour_start >= reservation.hour_end and hour_end > reservation.hour_end):
                continue
            else:
                raise ValidationError("На это время столик занят!")

        return cleaned_data
