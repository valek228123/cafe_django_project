from datetime import datetime
from re import search
from traceback import print_tb

from django.contrib.auth.decorators import login_not_required, login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, resolve_url, redirect
from django.views import generic
from requests import session

from reservation.models import Reservation
from .models import Table, Favorites
from django.utils.decorators import method_decorator
from authentication.models import User


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
    paginator = Paginator(tables, per_page)
    page = paginator.get_page(page_number)
    is_paginated = page.has_other_pages()
    if 8 <= hour <= 18:
        active_reservation = Reservation.objects.filter(date=data_now.date(),hour_start__lte=hour,hour_end__gt=hour).only('table_id')
        busy_tables_id = set(active_reservation.values_list('table_id', flat=True))
        if request.user.is_authenticated:
            favorites_tables_id = request.user.favorites_tables.all().values_list('id', flat=True)
        else:
            favorites_tables_id = []
        all_tables = [(table,table.id not in busy_tables_id,table.id in favorites_tables_id) for table in page.object_list]
    else:
        all_tables = [ (table, False) for table in page.object_list ]

    return render(request, 'tables/list_tables.html', context={'tables': all_tables,"list_of_seats":[ i for i in range(1,11) ],"page":page,"is_paginated":is_paginated})

@login_required
def favorites_post_view_post(request, table_id):
    if request.method == 'POST':
        referer_url = request.META.get('HTTP_REFERER')
        if Favorites.objects.filter(table_id=table_id, user_id=request.user.id).exists():
            Favorites.objects.filter(table_id=table_id, user_id=request.user.id).delete()
            return redirect(resolve_url(referer_url))
        Favorites.objects.create(user=request.user, table_id=table_id)
        return redirect(resolve_url(referer_url))



@login_required
def favorites_post_view_get(request):
    if request.method == 'GET':
        search = request.GET.get('search', "")
        seats = request.GET.get('seats')
        page_number = request.GET.get('page', 1)
        per_page = 12
        tables = request.user.favorites_tables.all().prefetch_related('feature')
        if search:
            tables = tables.filter(Q(number__icontains=search) | Q(seats__icontains=search))
        if seats:
            tables = tables.filter(seats=seats)
        data_now = datetime.now()
        hour = data_now.hour
        paginator = Paginator(tables, per_page)
        page = paginator.get_page(page_number)
        is_paginated = page.has_other_pages()
        if 8 <= hour <= 18:
            active_reservation = Reservation.objects.filter(date=data_now.date(), hour_start__lte=hour,
                                                            hour_end__gt=hour).only('table_id')
            busy_tables_id = set(active_reservation.values_list('table_id', flat=True))
            all_tables = [(table, table.id not in busy_tables_id) for table in page.object_list]
        else:
            all_tables = [(table, False) for table in page.object_list]
        return render(request, 'tables/list_favorite_table.html',
                      context={'tables': all_tables, "list_of_seats": [i for i in range(1, 11)], "page": page,
                               "is_paginated": is_paginated})
