from rest_framework import serializers

from authentication.models import User


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = ['id', 'username', 'email','first_name','last_name','last_login','date_joined','is_staff', 'is_superuser', 'is_active','password']
        read_only_fields = ['id','first_name','last_name','last_login','date_joined','is_staff', 'is_superuser', 'is_active',]
