from .serializers import BookingTimeSerializer
from rest_framework import status
from .models import  bookingTime
from rest_framework.views import APIView
from rest_framework.response import Response



class BookingTimeView(APIView):
    def get(self, request, *args, **kwargs):
            try:
                time_slot = bookingTime.objects.all()
                serializer = BookingTimeSerializer(time_slot,many=True)
                return Response({"time_data" :  serializer.data},status=status.HTTP_200_OK)

            except time_slot.DoesNotExist:
                return Response({"message": "Time slot not found"}, status=status.HTTP_404_NOT_FOUND)



