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
            # table = Tabel.objects.filter(id = table_id).get()
            # table.is_free  = False
            # table.save()
            return redirect(resolve_url('/tables/'))


    return render(request,"reservation/book_tabel.html", context = {"form":form,"table_id":table_id})
