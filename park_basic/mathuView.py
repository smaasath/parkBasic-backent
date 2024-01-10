from django.http import JsonResponse
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import JSONParser
from django.views.decorators.csrf import csrf_exempt
from .serializers import UserSerializer, ReserverSerializer,BookingSerializer
from django.contrib.auth.hashers import make_password
from rest_framework.authtoken.views import Token
from rest_framework import status
from .models import reserver, User,booking
from django.contrib.auth import authenticate


@api_view(['GET'])
@csrf_exempt
@parser_classes([JSONParser])
def GetAllBookingAPI(request):
    bookings = booking.objects.all()
    data = []

    for booking_instance in bookings:
        reserver_instance = booking_instance.reserverId
        if reserver_instance:
            user_instance = reserver_instance.userId

            if user_instance:
                user_data = {
                    'first_name': user_instance.first_name,
                    'last_name': user_instance.last_name,
                    'email': user_instance.email,
                }
                reserver_data = ReserverSerializer(reserver_instance).data
                booking_data = BookingSerializer(booking_instance).data
                all_data = {
                'booking_data': booking_data,
                'reserver_data' : reserver_data,
                'user_data' : user_data,

                }
                data.append(all_data)

    return JsonResponse({
        'bookings': data
    }, safe=False, status=200)
