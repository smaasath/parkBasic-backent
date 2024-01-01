from rest_framework import serializers
from park_basic.models import booking
from park_basic.models import reserver
from park_basic.models import bookingSlot
from django.contrib.auth.models import User


class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = booking
        fields = '__all__'

class ReserverSerializer(serializers.ModelSerializer):
    class Meta:
        model = reserver
        fields = '__all__'

class BookingSlotSerializer(serializers.ModelSerializer):
    class Meta:
        model = bookingSlot
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password', 'is_superuser', 'first_name', 'last_name', 'email']
        extra_kwargs = {
            'password': {
                'write_only': True,
            },
        }
