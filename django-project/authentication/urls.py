from django.contrib.auth.views import LogoutView
from django.urls import path
from . import views as auth_views

app_name = "authentication"

urlpatterns = [
    path('register', auth_views.register_view, name='register'),
    path('login', auth_views.LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
]