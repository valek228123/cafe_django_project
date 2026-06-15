from django.contrib.auth.hashers import make_password
from rest_framework import status
from rest_framework.generics import ListAPIView, CreateAPIView,ListCreateAPIView
from rest_framework.permissions import IsAdminUser, AllowAny
from rest_framework.response import Response

from .serializers import UserSerializer
from ..models import User
from .permissions import AdminAndUserPermission

class UserListApiView(ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AdminAndUserPermission]

    def perform_create(self, serializer):
        password = serializer.validated_data['password']
        serializer.save(password = make_password(password))


