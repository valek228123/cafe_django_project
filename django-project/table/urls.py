from django.urls import path
from . import views as table_views

app_name = 'table'
urlpatterns=[
    path('', table_views.table_view, name = 'list'),
    ]