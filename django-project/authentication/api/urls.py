from django.urls import path
from . import views

app_name = 'api:users'

urlpatterns = [
    path('',views.UserListApiView.as_view(),name='user-list-get'),
]