from django.contrib.auth.hashers import make_password
from rest_framework import status
from rest_framework.generics import ListAPIView, CreateAPIView,ListCreateAPIView
from rest_framework.permissions import IsAdminUser, AllowAny
from rest_framework.response import Response

from .serializers import UserSerializer
from ..models import User

class UserListApiView(ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        print(request.user, request.user.is_staff)
        if request.user and request.user.is_authenticated and request.user.is_staff:
            return super().get(request, *args, **kwargs)
        return Response(status=status.HTTP_403_FORBIDDEN)

    def perform_create(self, serializer):
        password = serializer.validated_data['password']
        serializer.save(password = make_password(password))


