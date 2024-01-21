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
            try:
                slot = bookingSlot.objects.get(id=pk)
                serializer = BookingSlotSerializer(slot,many=False)
                return Response({"data" : serializer.data})

            except bookingSlot.DoesNotExist:
                return Response({"message": "Booking slot not found"}, status=status.HTTP_404_NOT_FOUND)
        else:
            slots = bookingSlot.objects.all()
            serializer = BookingSlotSerializer(slots, many=True)
            return Response({"data" : serializer.data})

    def post(self, request, *args,**kwargs):
        userTokens = userView.userViewSet()
        provided_token = request.META.get('HTTP_AUTHORIZATION')
        isValidSuperToken = userTokens.validateSuperToken(provided_token)
        if isValidSuperToken:
            serializer = BookingSlotSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({"message": "Booking slot added successfully"}, status=status.HTTP_200_OK)
            else: return Response({"message" : serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        else:
            return Response({"message": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)


    def put(self, request, *args, **kwargs):
        userTokens = userView.userViewSet()
        provided_token = request.META.get('HTTP_AUTHORIZATION')
        isValidSuperToken = userTokens.validateSuperToken(provided_token)
        if isValidSuperToken:
            pk = kwargs.get('pk')
            try:
                slot = bookingSlot.objects.get(id=pk)
                serializer = BookingSlotSerializer(instance=slot, data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    return Response({"message": "Booking slot edit successfully"}, status=status.HTTP_200_OK)
                else:
                    return Response({"message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

            except bookingSlot.DoesNotExist:
                return Response({"message": "Booking slot not found"}, status=status.HTTP_404_NOT_FOUND)

        else:
            return Response({"message": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)


    def delete(self, request, *args,**kwargs):
        userTokens = userView.userViewSet()
        provided_token = request.META.get('HTTP_AUTHORIZATION')
        isValidSuperToken =userTokens.validateSuperToken(provided_token)
        if isValidSuperToken:
            pk = kwargs.get('pk')
            try:
                slot = bookingSlot.objects.get(id=pk)
                slot.delete()
                return Response({"message": "Booking slot deleted successfully"}, status=status.HTTP_200_OK)

            except bookingSlot.DoesNotExist:
                return Response({"message": "Booking slot not found"}, status=status.HTTP_404_NOT_FOUND)


        else:
            return Response({"message": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)

