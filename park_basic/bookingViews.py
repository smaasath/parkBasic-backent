from .serializers import UserSerializer, ReserverSerializer, BookingSerializer, bookingSlot
from rest_framework.authtoken.views import Token
from rest_framework import status
from .models import reserver, User, booking, bookingSlot
from rest_framework.views import APIView
from rest_framework.response import Response
from park_basic import userView
from django.utils import timezone


class BookingViewSet(APIView):

    def getAllUserBookingsDetail(self, bookings):
        data = []
        for booking_instance in bookings:
            bookingslot_instance = booking_instance.slotId

            if bookingslot_instance:
                bookingSlotData = {
                    'id': bookingslot_instance.id,
                    'slotName': bookingslot_instance.slotName
                }

                bookinTime_instance = booking_instance.timeId

                if bookinTime_instance:
                    bookingTimeData = {
                        'id': bookinTime_instance.id,
                        'bookingTime': bookinTime_instance.bookingTime
                    }

                    booking_data = BookingSerializer(booking_instance).data
                    all_data = {
                        'booking_data': booking_data,
                        'booking_slot_data': bookingSlotData,
                        'booking_time_data': bookingTimeData

                    }
                    data.append(all_data)

        return data

    def getAllDetailBooking(self, bookings):
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

                    bookingslot_instance = booking_instance.slotId

                    if bookingslot_instance:
                        bookingSlotData = {
                            'id' : bookingslot_instance.id,
                            'slotName' : bookingslot_instance.slotName
                        }

                        bookinTime_instance = booking_instance.timeId

                        if bookinTime_instance:
                            bookingTimeData = {
                                'id' : bookinTime_instance.id,
                                'bookingTime' : bookinTime_instance.bookingTime
                            }

                            reserver_data = ReserverSerializer(reserver_instance).data
                            booking_data = BookingSerializer(booking_instance).data
                            all_data = {
                                'booking_data': booking_data,
                                'reserver_data': reserver_data,
                                'user_data': user_data,
                                'booking_slot_data': bookingSlotData,
                                'booking_time_data': bookingTimeData

                            }
                            data.append(all_data)

        return data

    def getBookingDetails(self, booking_instance):
        reserver_instance = booking_instance.reserverId
        if reserver_instance:
            user_instance = reserver_instance.userId

            if user_instance:
                user_data = {
                    'first_name': user_instance.first_name,
                    'last_name': user_instance.last_name,
                    'email': user_instance.email,
                }

                bookingslot_instance = booking_instance.slotId

                if bookingslot_instance:
                    bookingSlotData = {
                        'id': bookingslot_instance.id,
                        'slotName': bookingslot_instance.slotName
                    }

                    bookinTime_instance = booking_instance.timeId

                    if bookinTime_instance:
                        bookingTimeData = {
                            'id': bookinTime_instance.id,
                            'bookingTime': bookinTime_instance.bookingTime
                        }

                        reserver_data = ReserverSerializer(reserver_instance).data
                        booking_data = BookingSerializer(booking_instance).data
                        all_data = {
                            'booking_data': booking_data,
                            'reserver_data': reserver_data,
                            'user_data': user_data,
                            'booking_slot_data': bookingSlotData,
                            'booking_time_data': bookingTimeData

                        }
                        return all_data
        return None


    def get(self, request, *args, **kwargs):
        userTokens = userView.userViewSet()
        provided_token = request.META.get('HTTP_AUTHORIZATION')
        isValidSuperToken = userTokens.validateSuperToken(provided_token)
        isVaidToken = userTokens.validateToken(provided_token)

        if isValidSuperToken:
            pk = kwargs.get('pk')
            if pk:
                try:
                    Booking = booking.objects.get(id=pk)
                    data = self.getBookingDetails(Booking)
                    return Response({"data": data})
                except booking.DoesNotExist:
                    return Response({"message": "Booking not found"}, status=status.HTTP_404_NOT_FOUND)
            else:
                bookings = booking.objects.all()
                data = self.getAllDetailBooking(bookings)
                return Response({"data": data})

        elif isVaidToken:
            try:
                Reserver = reserver.objects.get(userId=isVaidToken.id)
                userBookings = booking.objects.filter(reserverId=Reserver.id)
                data = self.getAllUserBookingsDetail(userBookings)
                return Response({"data": data},status=status.HTTP_200_OK)

            except reserver.DoesNotExist:
                return Response({"message": "Reserver Not Found"}, status=status.HTTP_404_NOT_FOUND)

        else:
            return Response({"message": "unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)




    def post(self, request, *args, **kwargs):
        userTokens = userView.userViewSet()
        provided_token = request.META.get('HTTP_AUTHORIZATION')
        isValidToken = userTokens.validateToken(provided_token)

        if isValidToken:
            current_time = timezone.now().time()
            current_date = timezone.now().date()
            Reserver = reserver.objects.filter(userId=isValidToken.id).first()
            reserver_id = Reserver.id
            booking_serializer = BookingSerializer(data={
                "Date": current_date,
                "Time": current_time,
                "reserverId": reserver_id,
                "timeId": request.data.get('timeId'),
                "slotId": request.data.get('slotId')
            })
            bookings = booking.objects.filter(Date=current_date,
                                              timeId=request.data.get('timeId'),
                                              slotId=request.data.get('slotId')).first()

            if bookings:
                return Response({"message": "Already Slots Booked"}, status=status.HTTP_400_BAD_REQUEST)

            else:
                if booking_serializer.is_valid():
                    if booking_serializer.save():
                        return Response({"message": "Booking Booked successfully"}, status=status.HTTP_200_OK)
                    else:
                        return Response({"message": "Booked Failed"}, status=status.HTTP_400_BAD_REQUEST)

                else:
                    return Response({"message": booking_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        else:
            return Response({"message": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)

    def delete(self, request, *args, **kwargs):
        userTokens = userView.userViewSet()
        provided_token = request.META.get('HTTP_AUTHORIZATION')
        isValidSuperToken = userTokens.validateSuperToken(provided_token)
        if isValidSuperToken:
            pk = kwargs.get('pk')
            try:
                booking_instance = booking.objects.get(id=pk)
                booking_instance.delete()
                return Response({"message": "Booking deleted successfully"}, status=status.HTTP_200_OK)
            except booking.DoesNotExist:
                return Response({"message": "Booking not found"}, status=status.HTTP_404_NOT_FOUND)


        else:
            return Response({"message": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)
