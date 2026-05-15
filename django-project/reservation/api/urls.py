from . import views
from django.urls import path


app_name = "api:reservations"
urlpatterns = [
    path('', views.ReservationApiView.as_view(), name='reservations-list'),
    path('<int:reservation_id>', views.DetailReservationApiView.as_view(), name='reservations-detail'),
    path('my/', views.ReservationApiViewMy.as_view(), name='reservations-list-my'),
]