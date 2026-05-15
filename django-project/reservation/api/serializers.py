from rest_framework import serializers
from rest_framework.relations import PrimaryKeyRelatedField

from authentication.models import User
from reservation.models import Reservation
from table.models import Table


class ShortUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class ShortTableSerializer(serializers.ModelSerializer):
    feature = serializers.SlugRelatedField(many=True, read_only=True, slug_field='name')
    class Meta:
        model = Table
        fields = ['id','number','seats','feature']


class ReservationSerializer(serializers.ModelSerializer):
    user = ShortUserSerializer(read_only=True)
    table = PrimaryKeyRelatedField(queryset=Table.objects.all(),write_only=True)
    table_details = ShortTableSerializer(source='table',read_only=True,label='table')
    class Meta:
        model = Reservation
        fields = ['id','date','created_at','hour_start','hour_end','user','table','table_details']
        read_only_fields = ['id',"user",'created_at']








