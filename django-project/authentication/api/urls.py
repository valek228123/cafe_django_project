from django.urls import path
from . import views

app_name = 'api_users'

urlpatterns = [
    path('',views.UserListApiView.as_view(),name='user-list'),
]