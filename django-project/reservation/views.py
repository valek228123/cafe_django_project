from django.shortcuts import render, redirect, resolve_url
from .forms import ReservationForm
from django.contrib.auth.decorators import login_required
from .models import Reservation
from table.models import Tabel


@login_required
def book_table_view(request,table_id):
    form = ReservationForm()
    if request.method == 'POST':
        form = ReservationForm(request.POST)
        if form.is_valid():
            book_tabel = Reservation.objects.create(
                tabel_id=table_id,
                user_id=request.user.id,
                date = form.cleaned_data['date'],
                hour_start = form.cleaned_data['hour_start'],
                hour_end = form.cleaned_data['hour_end'],
            )
            return redirect(resolve_url('/tables/list_booked_tables'))


    return render(request,"reservation/book_tabel.html", context = {"form":form,"table_id":table_id})

@login_required
def list_booked_tables_view(request):
    reservations = Reservation.objects.filter(user_id=request.user.id).select_related('tabel').order_by('date', 'hour_start')
    return render(request, 'tabels/list_booked_tables.html', context = {'reservations': reservations})

@login_required
def delete_booked_table_view(request,reservation_id):
    if request.method == 'POST':
        Reservation.objects.get(id = reservation_id,user_id=request.user.id).delete()
        return redirect(resolve_url('/tables/list_booked_tables'))
