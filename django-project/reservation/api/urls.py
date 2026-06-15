from . import views
from django.urls import path
from rest_framework import routers
router = routers.DefaultRouter()
router.register('my', views.ReservationApiViewSetMy,basename='reservation_my')
router.register('', views.ReservationApiViewSet,basename='reservation')

app_name = "api:reservations"
# urlpatterns = [
#     path('', views.ReservationApiViewV1.as_view(), name='reservations-list'),
#     path('<int:reservation_id>', views.DetailReservationApiView.as_view(), name='reservations-detail'),
#     path('my/', views.ReservationApiViewMy.as_view(), name='reservations-list-my'),
# ]