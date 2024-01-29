from .serializers import UserSerializer, ReserverSerializer, BookingSerializer, bookingSlot
from rest_framework.authtoken.views import Token
from rest_framework import status, viewsets
from .models import reserver, User, booking, bookingSlot
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import ReserverSerializer, UserSerializer


class userViewSet(APIView):
    def validateSuperToken(self, token):
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

    def validateToken(self, token):
        if token and token.startswith('Bearer '):
            token_key = token.split(' ')[1]
            try:
                token_obj = Token.objects.get(key=token_key)
                user = token_obj.user
                return user
            except Token.DoesNotExist:
                return False
        else:
            return False

    def get(self, request, *args, **kwargs):
        provided_token = request.META.get('HTTP_AUTHORIZATION')
        isValidToken = self.validateToken(provided_token)

        if isValidToken:
            userId = isValidToken.id
            userInstance = UserSerializer(instance=isValidToken)
            userData = userInstance.data
            try:
                Reserver = reserver.objects.get(userId=userId)
                ReserverInstance = ReserverSerializer(instance=Reserver)
                return Response({"user": userData,
                                 "reserver": ReserverInstance.data}, status=status.HTTP_200_OK)
            except reserver.DoesNotExist:
                return Response({"user": userData,
                                 }, status=status.HTTP_200_OK)
        else:
            return Response({"message": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)

    def put(self, request, *args, **kwargs):
        provided_token = request.META.get('HTTP_AUTHORIZATION')
        isValidToken = self.validateToken(provided_token)

        if isValidToken:
            try:
                userId = isValidToken.id
                user_data = request.data.get('user', {})
                reserver_data = request.data.get('reserver', {})


                if 'oldpassword' in user_data:
                    oldpassword = user_data.get('oldpassword')
                    newpassword = user_data.get('password')

                    passs = {"password": newpassword}

                    # Check if the provided old password matches the existing user password
                    if isValidToken.check_password(oldpassword):
                        isValidToken.set_password(newpassword)
                        isValidToken.save()
                        return Response({"message": "Password updated successfully"}, status=status.HTTP_200_OK)


                    else:
                        return Response({"error": "Incorrect old password"}, status=status.HTTP_400_BAD_REQUEST)

                else:
                    reserverInstance = reserver.objects.get(userId=userId)
                    userInstance = UserSerializer(instance=isValidToken, data=user_data, partial=True)
                    if userInstance.is_valid():
                        userInstance.save()
                        reserverInstance = ReserverSerializer(instance=reserverInstance, data=reserver_data, partial=True)
                        if reserverInstance.is_valid():
                            reserverInstance.save()
                            return Response({"message": "user updated successfully"}, status=status.HTTP_200_OK)
                        else:
                            return Response({"message": reserverInstance.errors}, status=status.HTTP_400_BAD_REQUEST)
                    else:
                        return Response({"Message": userInstance.errors}, status=status.HTTP_400_BAD_REQUEST)


            except reserver.DoesNotExist:
                return Response({"message": "user not found"}, status=status.HTTP_404_NOT_FOUND)

        else:
            return Response({"message": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)

    def delete(self, request, *args, **kwargs):
        provided_token = request.META.get('HTTP_AUTHORIZATION')
        isValidToken = self.validateToken(provided_token)
        if isValidToken:

            try:
                Reserver = reserver.objects.get(userId=isValidToken.id)
                Reserver.delete()
                isValidToken.delete()
                return Response({"message": "user deleted successfully"}, status=status.HTTP_200_OK)

            except reserver.DoesNotExist:
                return Response({"message": "user not found"}, status=status.HTTP_404_NOT_FOUND)


        else:
            return Response({"message": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)
