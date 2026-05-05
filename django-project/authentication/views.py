from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect, resolve_url
from django.views import View
from django.contrib.auth.decorators import login_not_required
from authentication.forms import RegisterForm
from .models import User

# Create your views here.


class LoginView(LoginView):
    template_name = "auth/login.html"

@login_not_required
def register_view(request):
    form = RegisterForm()
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            User.objects.create_user(
                username=form.cleaned_data['username'],
                password = form.cleaned_data['password']
            )
            return redirect(resolve_url('authentication:login'))
    return render(request,"auth/register.html", context = {"form":form})

