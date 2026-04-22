from django.shortcuts import render
from .models import Tabel



# Create your views here.




def index_view(request):
    return render(request,'index.html')

def tabels_view(request):
    tabels = Tabel.objects.all()

    return render(request, 'tabels/list_tabels.html', context = {'tabels':tabels})