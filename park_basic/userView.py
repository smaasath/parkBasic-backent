from .serializers import UserSerializer, ReserverSerializer, BookingSerializer,bookingSlot
from rest_framework.authtoken.views import Token
from rest_framework import status, viewsets
from .models import reserver, User,booking,bookingSlot
from rest_framework.views import APIView
from rest_framework.response import Response

class userViewSet(APIView):
    def validateSuperToken(token):
        if token and token.startswith('Bearer '):
            token_key = token.split(' ')[1]
            try:
                token_obj = Token.objects.get(key=token_key)
                user = token_obj.user
                if user.is_superuser == 1:
                    return True
                else:
                    return False
            except Token.DoesNotExist:
                return False
        else:
            return False

    def validateToken(token):
        if token and token.startswith('Bearer '):
            token_key = token.split(' ')[1]
            try:
                token_obj = Token.objects.get(key=token_key)
                user = token_obj.user
                return True
            except Token.DoesNotExist:
                return False
        else:
            return False

