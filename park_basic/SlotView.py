from .serializers import BookingSlotSerializer
from rest_framework.authtoken.views import Token
from rest_framework import status
from .models import bookingSlot
from rest_framework.views import APIView
from rest_framework.response import Response


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
        serializer = BookingSlotSerializer(data=request.data)
        provided_token = request.META.get('HTTP_AUTHORIZATION')
        if provided_token and provided_token.startswith('Bearer '):
            token_key = provided_token.split(' ')[1]
            try:
                token = Token.objects.get(key=token_key)
                user = token.user
                if (user.is_superuser == 1):
                    if serializer.is_valid():
                        serializer.save()
                        return Response({"message" : "Booking slot added successfully"}, status=status.HTTP_200_OK)
                    else:
                        return Response({"message" : serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

                else: return Response({"message" : "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)

            except Token.DoesNotExist:
                return Response({"message" : "Invalid Token"}, status=status.HTTP_401_UNAUTHORIZED)

        else: return Response({"message" : "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)

    def put(self, request, *args, **kwargs):
        provided_token = request.META.get('HTTP_AUTHORIZATION')
        if provided_token and provided_token.startswith('Bearer '):
            token_key = provided_token.split(' ')[1]
            try:
                token = Token.objects.get(key=token_key)
                user = token.user
                if user.is_superuser == 1:
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

            except Token.DoesNotExist:
                return Response({"message": "Invalid Token"}, status=status.HTTP_401_UNAUTHORIZED)

        else:
            return Response({"message": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)


    def delete(self, request, *args,**kwargs):
        provided_token = request.META.get('HTTP_AUTHORIZATION')
        if provided_token and provided_token.startswith('Bearer '):
            token_key = provided_token.split(' ')[1]
            try:
                token = Token.objects.get(key=token_key)
                user = token.user
                if (user.is_superuser == 1):
                    pk = kwargs.get('pk')
                    slot = bookingSlot.objects.get(id=pk)
                    if slot.delete():
                        return Response({"message": "Booking slot deleted successfully"}, status=status.HTTP_200_OK)
                    else:
                        return Response({"message": "Booking slot not Delete"}, status=status.HTTP_400_BAD_REQUEST)

                else:
                    return Response({"message": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)

            except Token.DoesNotExist:
                return Response({"message": "Invalid Token"}, status=status.HTTP_401_UNAUTHORIZED)

        else:
            return Response({"message": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)

