from datetime import datetime
from re import search

from django.contrib.auth.decorators import login_not_required, login_required
from django.shortcuts import render
from django.views import generic

from reservation.models import Reservation
from .models import Table
from django.utils.decorators import method_decorator


# Create your views here.



@method_decorator(login_not_required, name='dispatch')
class IndexView(generic.TemplateView):
    template_name = 'index.html'

@login_not_required
def table_view(request):
    tables = Table.objects.all()

    # tables = tables.filter(description__icontains="Гармония")
    data_now = datetime.now()
    hour = data_now.hour
    print(hour)
    if 8 <= hour <= 18:
        all_tables = []
        for table in tables:
            is_free = True
            reservations = Reservation.objects.filter(date=data_now.date(), table_id=table.id)
            for reservation in reservations:
                if reservation.hour_start <= hour < reservation.hour_end:
                    is_free = False
                    break
            all_tables.append((table, is_free))
    else:
        all_tables = [ (table, False) for table in tables ]
    return render(request, 'tables/list_tables.html', context={'tables': all_tables})


