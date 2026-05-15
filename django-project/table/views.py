from datetime import datetime
from re import search

from django.contrib.auth.decorators import login_not_required, login_required
from django.core.paginator import Paginator
from django.db.models import Q
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
    search = request.GET.get('search',"")
    seats = request.GET.get('seats')
    page_number = request.GET.get('page',1)
    per_page = 12
    tables = Table.objects.all().prefetch_related('feature')
    if search:
        tables = tables.filter(Q(number__icontains=search) | Q(seats__icontains=search))
    if seats:
        tables = tables.filter(seats=seats)
    data_now = datetime.now()
    hour = data_now.hour
    if 8 <= hour <= 18:
        # all_tables = []
        # for table in tables:
        #     is_free = True
        #     reservations = Reservation.objects.filter(table_id=table.id,date=data_now)
        #     for reservation in reservations:
        #         if reservation.table_id ==  table.id and reservation.hour_start <= hour < reservation.hour_end:
        #             is_free = False
        #             break
        #     all_tables.append((table, is_free))
        active_reservation = Reservation.objects.filter(date=data_now.date(),hour_start__lte=hour,hour_end__gt=hour).only('table_id')
        busy_tables_id = set(active_reservation.values_list('table_id', flat=True))
        paginator = Paginator(tables,per_page)
        page = paginator.get_page(page_number)
        is_paginated = page.has_other_pages()
        all_tables = [(table,table.id not in busy_tables_id) for table in page.object_list]
    else:
        paginator = Paginator(tables, per_page)
        page = paginator.get_page(page_number)
        is_paginated = page.has_other_pages()
        all_tables = [ (table, False) for table in page.object_list ]
    return render(request, 'tables/list_tables.html', context={'tables': all_tables,"list_of_seats":[ i for i in range(1,11) ],"page":page,"is_paginated":is_paginated})


