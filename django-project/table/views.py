from django.contrib.auth.decorators import login_not_required
from django.shortcuts import render
from .models import Tabel



# Create your views here.



@login_not_required
def index_view(request):
    return render(request,'index.html')
@login_not_required
def table_view(request):
    tables = Tabel.objects.all()
    return render(request, 'tabels/list_tabels.html', context = {'tables':tables})