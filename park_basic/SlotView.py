from .serializers import BookingSlotSerializer
from rest_framework import status
from .models import bookingSlot
from rest_framework.views import APIView
from rest_framework.response import Response
from park_basic import userView


class BookingSlotView(APIView):
    def get(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        if pk:
            slot = bookingSlot.objects.filter(id=pk).first()
            if slot:
                serializer = BookingSlotSerializer(slot,many=False)
                return Response({"data" : serializer.data})
            else: return Response({"message" : "No such slot"},status=status.HTTP_400_BAD_REQUEST)
        else:
            slots = bookingSlot.objects.all()
            serializer = BookingSlotSerializer(slots, many=True)
            return Response({"data" : serializer.data})

    def post(self, request, *args,**kwargs):
        provided_token = request.META.get('HTTP_AUTHORIZATION')
        isValidSuperToken = userView.userViewSet.validateSuperToken(provided_token)
        if isValidSuperToken:
            serializer = BookingSlotSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({"message": "Booking slot added successfully"}, status=status.HTTP_200_OK)
            else: return Response({"message" : serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        else:
            return Response({"message": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)


    def put(self, request, *args, **kwargs):
        provided_token = request.META.get('HTTP_AUTHORIZATION')
        isValidSuperToken = userView.userViewSet.validateSuperToken(provided_token)
        if isValidSuperToken:
            pk = kwargs.get('pk')
            slot = bookingSlot.objects.get(id=pk)
            serializer = BookingSlotSerializer(instance=slot, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({"message": "Booking slot edit successfully"}, status=status.HTTP_200_OK)
            else:
                return Response({"message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        else:
            return Response({"message": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)


    def delete(self, request, *args,**kwargs):
        provided_token = request.META.get('HTTP_AUTHORIZATION')
        isValidSuperToken = userView.userViewSet.validateSuperToken(provided_token)
        if isValidSuperToken:
            pk = kwargs.get('pk')
            slot = bookingSlot.objects.get(id=pk)
            if slot.delete():
                return Response({"message": "Booking slot deleted successfully"}, status=status.HTTP_200_OK)
            else:
                return Response({"message": "Booking slot not Delete"}, status=status.HTTP_400_BAD_REQUEST)


        else:
            return Response({"message": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)

