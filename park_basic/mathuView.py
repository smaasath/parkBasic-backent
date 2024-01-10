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
    for booking_instance in bookings:
        reserver_instance = booking_instance.reserverId
        if reserver_instance:
            reserver_data = {
                'carNo': reserver_instance.carNo,
                'phnNo': reserver_instance.phnNo,
                # Add other fields as needed
            }
            # print(reserver_instance.carNo)
            booking_instance.reserverId = JsonResponse({reserver_data})
    bookings_serializer=BookingSerializer(bookings,many=True)
    return JsonResponse({
        'bookings': bookings_serializer.data
    }, safe=False, status=200)
