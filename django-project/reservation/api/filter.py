from django_filters import rest_framework as filters

from reservation.models import Reservation


class FilterClass(filters.FilterSet):
    table__number = filters.CharFilter(field_name='table__number',label='Number of tables')
    date = filters.DateFilter(field_name='date',label='Date')

    class Meta:
        model = Reservation
        fields = ['table__number','date']

