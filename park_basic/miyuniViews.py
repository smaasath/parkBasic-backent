from django.shortcuts import render

from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse
from .serializers import BookingSerializer
from .models import booking

@csrf_exempt
def bookingApi(request,id=0):
    #get specific booking details
    if request.method=='GET':
        booking = booking.objects.get(id=id)
        booking_serializer=BookingSerializer(booking,many=True)
        return JsonResponse(booking_serializer.data,safe=False)

    #update booking details
    elif request.method=='PUT':
        booking_data=JSONParser().parse(request)
        booking=booking.objects.get(id=id)
        booking_serializer=bookingSerializer(booking,data=booking_data)
        if booking_serializer.is_valid():
            booking_serializer.save()
            return JsonResponse("Updated Successfully",safe=False)
        return JsonResponse("Failed to Update")
   