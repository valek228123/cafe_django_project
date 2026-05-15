from datetime import datetime

from django.core.paginator import Paginator
from django.shortcuts import render, redirect, resolve_url
from django.utils.decorators import method_decorator

from .forms import ReservationForm
from django.contrib.auth.decorators import login_required
from .models import Reservation
from django.db.models.query import Q
from django.views.generic import ListView


@login_required
def book_table_view(request, table_id):
    form = ReservationForm()
    if request.method == 'POST':
        form = ReservationForm(request.POST)
        if form.is_valid():
            Reservation.objects.create(
                table_id=table_id,
                user_id=request.user.id,
                date=form.cleaned_data['date'],
                hour_start=form.cleaned_data['hour_start'],
                hour_end=form.cleaned_data['hour_end'],
            )
            return redirect(resolve_url('/reservation/list_booked_tables'))

    return render(request, "reservation/book_table.html", context={"form": form, "table_id": table_id})


@login_required
def list_booked_tables_view(request):
    search = request.GET.get('search',"").strip()
    page_number = request.GET.get('page',1)
    per_page = 12
    reservations_qs = Reservation.objects.all()
    if search:
        try:
            search_date = datetime.strptime(search, '%d.%m.%Y').date()
            reservations_qs = reservations_qs.filter(
                Q(table__number__icontains=search) | Q(date__icontains=search_date))
        except ValueError:
            reservations_qs = reservations_qs.filter(date__icontains=search)
    reservations_qs = reservations_qs.filter(user_id=request.user.id)
    reservations_qs = reservations_qs.select_related('table').order_by('date', 'hour_start')
    reservations_qs = reservations_qs.only('date', 'hour_start', 'hour_end', 'table__number', "table__seats")
    paginator = Paginator(reservations_qs, per_page)
    page = paginator.get_page(page_number)
    is_paginated = page.has_other_pages()
    return render(request, 'reservation/list_booked_tables.html', context={'reservations': reservations_qs,"page":page,"is_paginated":is_paginated})


@method_decorator(login_required, name='dispatch')
class TableListView(ListView):
    template_name = 'reservation/list_booked_tables.html'
    context_object_name = 'reservations'
    paginate_by = 12

    def get_queryset(self):
        search = self.request.GET.get('search',"")
        reservations_qs = Reservation.objects.all()
        if search:
            try:
                search_date = datetime.strptime(search, '%d.%m.%Y').date()
                reservations_qs = reservations_qs.filter(
                    Q(table__number__icontains=search) | Q(date__icontains=search_date))
            except ValueError:
                reservations_qs = reservations_qs.filter(date__icontains=search)
        reservations_qs = reservations_qs.filter(user_id=self.request.user.id)
        reservations_qs = reservations_qs.select_related('table').order_by('date', 'hour_start')
        reservations_qs = reservations_qs.only('date', 'hour_start', 'hour_end', 'table__number', "table__seats")
        return reservations_qs


@login_required
def delete_booked_table_view(request, reservation_id):
    if request.method == 'POST':
        Reservation.objects.get(id=reservation_id, user_id=request.user.id).delete()
        return redirect(resolve_url('/reservation/list_booked_tables'))
