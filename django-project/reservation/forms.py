from django import forms
from django.core.exceptions import ValidationError
from reservation.models import Reservation


class ReservationForm(forms.ModelForm):
    class Meta:

        model = Reservation
        fields = ['date', 'hour_start', 'hour_end']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'hour_start': forms.NumberInput(attrs={'placeholder': 'Например 12','min': '8', 'max': '18'}),
            'hour_end': forms.NumberInput(attrs={'placeholder': 'Например 12','min': '8', 'max': '18'}),
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

        if hour_start and hour_end:
            if hour_start >= hour_end:
                raise ValidationError("Время начала должно быть раньше времени конца!")
        return cleaned_data

    # widgets = {
    #     'date': forms.DateInput(attrs={'type': 'date'}),
    #     'hour_start': forms.NumberInput(attrs={
    #         'placeholder': 'Например: 12',
    #         'min': '8',
    #         'max': '18'
    #     }),
    #     'hour_end': forms.NumberInput(attrs={
    #         'placeholder': 'Например: 14',
    #         'min': '8',
    #         'max': '18'
    #     }),
    # }
