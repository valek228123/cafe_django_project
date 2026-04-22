from django.shortcuts import render
from .forms import ReservationForm


def book_table_view(request):
    form = ReservationForm()
    return render(request,"reservation/book_tabel.html", context = {"form":form})
