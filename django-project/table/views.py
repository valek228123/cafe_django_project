from datetime import datetime

from django.contrib.auth.decorators import login_not_required, login_required
from django.shortcuts import render

from reservation.models import Reservation
from .models import Tabel


# Create your views here.


@login_not_required
def index_view(request):
    return render(request, 'index.html')


@login_not_required
def table_view(request):
    tables = Tabel.objects.all()
    data_now = datetime.now()
    hour = data_now.hour
    if hour <= 18 or hour >= 8:
        all_tables = []
        for table in tables:
            is_free = True
            reservations = Reservation.objects.filter(date=data_now.date(), tabel_id=table.id)
            for reservation in reservations:
                if reservation.hour_start <= hour < reservation.hour_end:
                    is_free = False
                    break
            all_tables.append((table, is_free))
    return render(request, 'tabels/list_tabels.html', context={'tables': all_tables})


