from django.contrib.auth.hashers import make_password
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect, resolve_url
from django.views import View
from django.contrib.auth.decorators import login_not_required, login_required
from authentication.forms import RegisterForm, PasswordResetRequestForm,PasswordResetForm
from .models import User, PasswordResetToken
from django.conf import settings
from django.core.mail import send_mail
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.contrib.auth import logout
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
                password=form.cleaned_data['password']
            )
            return redirect(resolve_url('authentication:login'))
    return render(request, "auth/register.html", context={"form": form})


@login_required
def reset_request_password_view(request):
    form = PasswordResetRequestForm(user=request.user)
    is_good = False
    if request.method == 'POST':
        form = PasswordResetRequestForm(request.POST, user=request.user)
        if form.is_valid():
            token = PasswordResetToken.objects.create(
                user=form.user,
            )
            send_mail(
                subject="Смена пароля",
                message=f"Для смены пароля перейдите по ссылке http://127.0.0.1:8000/auth/reset-password/{token.token}",
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[form.cleaned_data['email']],
            )
            is_good = True
    return render(request, "auth/reset_request_password.html", context={"form": form, "is_good": is_good})


@login_required
def reset_password_view(request, token):
    token_db = get_object_or_404(PasswordResetToken, token=token)
    if  request.user == token_db.user:
        form = PasswordResetForm()
        if request.method == 'POST':
            form = PasswordResetForm(request.POST,user = request.user)
            if form.is_valid():
                User.objects.filter(id = request.user.id).update(password= make_password(form.cleaned_data['password']))
                logout(request)
                return redirect(resolve_url('index'))

        return render(request, "auth/reset_password.html", context={"form": form,"token":token})
    else:
        raise Http404