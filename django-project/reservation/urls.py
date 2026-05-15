from django.urls import path
from . import views as reservation_views

app_name = "reservation"
urlpatterns = [
    path('book_a_table/<int:table_id>', reservation_views.book_table_view, name='book-table'),
    path('list_booked_tables', reservation_views.list_booked_tables_view, name='list-booked-tables'),
    path('list_booked_tables/delete/<int:reservation_id>', reservation_views.delete_booked_table_view,
         name='delete-booked-table'),
]

