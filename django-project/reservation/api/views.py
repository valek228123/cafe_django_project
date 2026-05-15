from rest_framework import status, viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import GenericAPIView, ListCreateAPIView, CreateAPIView, RetrieveAPIView, \
    RetrieveUpdateDestroyAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly, IsAdminUser
from rest_framework.response import Response

import reservation
from .serializers import ReservationSerializer
from ..models import Reservation
from .permissions import OnlyReservationOwner, OnlyReservationOwnerOrReadOnly
from .filter import FilterClass


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticatedOrReadOnly])
def reservations_api_view(request):
    if request.method == 'GET':
        reservations = Reservation.objects.all()[:10]
        serializer = ReservationSerializer(reservations, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        print("request.data", request.data)
        serializer = ReservationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if serializer.validated_data['hour_start'] < serializer.validated_data['hour_end']:
            reservation = serializer.save(user=request.user)
            return Response(ReservationSerializer(reservation).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ReservationApiViewV1(GenericAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = ReservationSerializer
    queryset = Reservation.objects.all()[:10]

    def get(self, request, *args, **kwargs):
        reservations = self.get_queryset()
        serializer = self.get_serializer(reservations, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if serializer.validated_data['hour_start'] < serializer.validated_data['hour_end'] and (
                8 <= serializer.validated_data['hour_start'] < 18) and (
                8 <= serializer.validated_data['hour_end'] < 18):
            reservation = serializer.save(user=self.request.user)
            return Response(ReservationSerializer(reservation).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ReservationApiView(ListCreateAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    filterset_class = FilterClass
    queryset = (Reservation.objects.all().select_related("user").select_related("table").prefetch_related(
        "table__feature").only("id",
                               "date",
                               "created_at",
                               "hour_start",
                               "hour_end",
                               "user__username",
                               "user__email",
                               "table__number",
                               "table__seats"))
    serializer_class = ReservationSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ReservationApiViewMy(ListCreateAPIView):
    permission_classes = [OnlyReservationOwner]
    serializer_class = ReservationSerializer

    def get_queryset(self):
        return (Reservation.objects.all().select_related("user").select_related("table").prefetch_related(
            "table__feature").only("id",
                                   "date",
                                   "created_at",
                                   "hour_start",
                                   "hour_end",
                                   "user__username",
                                   "user__email",
                                   "table__number",
                                   "table__seats").filter(user=self.request.user))

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


@api_view(['GET', 'DELETE', 'PUT', 'PATCH'])
@permission_classes([IsAuthenticatedOrReadOnly])
def detail_reservations_api_view(request, reservation_id):
    reservation = (Reservation.objects.all().select_related("user").select_related("table").prefetch_related(
        "table__feature").only("id",
                               "date",
                               "created_at",
                               "hour_start",
                               "hour_end",
                               "user__username",
                               "user__email",
                               "table__number",
                               "table__seats").filter(id=reservation_id))
    if request.method == 'GET':
        serializer = ReservationSerializer(reservation)
        return Response(serializer.data)
    elif request.method == 'DELETE':
        reservation.delete()
        return Response(ReservationSerializer(reservation).data, status=status.HTTP_204_NO_CONTENT)
    elif request.method == 'PUT':
        serializer = ReservationSerializer(reservation, data=request.data)
        serializer.is_valid(raise_exception=True)
        if serializer.validated_data['hour_start'] < serializer.validated_data['hour_end']:
            reservation = serializer.save()
            return Response(ReservationSerializer(reservation).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'PATCH':
        serializer = ReservationSerializer(reservation, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        reservation = serializer.save()
        return Response(ReservationSerializer(reservation).data)


class DetailReservationApiView(RetrieveUpdateDestroyAPIView):
    queryset = (Reservation.objects.all().select_related("user").select_related("table").prefetch_related(
        "table__feature").only("id",
                               "date",
                               "created_at",
                               "hour_start",
                               "hour_end",
                               "user__username",
                               "user__email",
                               "table__number",
                               "table__seats"))
    serializer_class = ReservationSerializer
    permission_classes = [OnlyReservationOwnerOrReadOnly]
    filterset_class = FilterClass
    lookup_field = 'id'
    lookup_url_kwarg = 'reservation_id'

    def update(self, request, *args, **kwargs):
        super().update(request, *args, **kwargs)
        return Response(status=status.HTTP_201_CREATED)

    def patch(self, request, *args, **kwargs):
        super().patch(request, *args, **kwargs)
        return Response(status=status.HTTP_200_OK)
