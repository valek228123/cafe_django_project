from django.urls import path
from . import views as table_views

app_name = 'table'
urlpatterns=[
    path('', table_views.table_view, name = 'list'),
    path('favorites/<int:table_id>', table_views.favorites_post_view_post, name = 'favorites-post'),
    path('favorites',table_views.favorites_post_view_get, name = 'favorites-get'),

    ]