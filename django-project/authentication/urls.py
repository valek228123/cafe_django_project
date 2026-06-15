from django.contrib.auth.views import LogoutView
from django.urls import path
from . import views as auth_views

app_name = "authentication"

urlpatterns = [
    path('password-reset-request', auth_views.reset_request_password_view, name='password_reset_request'),
    path('reset-password/<uuid:token>', auth_views.reset_password_view, name='password_reset'),
    path('register', auth_views.register_view, name='register'),
    path('login', auth_views.LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
]