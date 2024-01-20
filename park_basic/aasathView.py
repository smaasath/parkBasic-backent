from django.http import JsonResponse
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import JSONParser
from django.views.decorators.csrf import csrf_exempt
from rest_framework.status import HTTP_400_BAD_REQUEST
from django.core.serializers import serialize
from .serializers import BookingSlotSerializer, BookingSerializer
from django.contrib.auth.hashers import make_password
from rest_framework.authtoken.views import Token
from rest_framework import status
from .models import bookingSlot
from django.contrib.auth import authenticate


@api_view(['GET','POST','PUT','DELETE'])
@csrf_exempt
@parser_classes([JSONParser])
def BookinSlotCRUD(request):
    if request.method == 'POST':
        data = JSONParser().parse(request)
        slotName = data.get("slotName")
        provided_token = request.META.get('HTTP_AUTHORIZATION')
        if provided_token and provided_token.startswith('Bearer '):
            token_key = provided_token.split(' ')[1]
            try:
                token = Token.objects.get(key=token_key)
                user = token.user
                if(user.is_superuser == 1):
                    slot_serializer = BookingSlotSerializer(data={
                        "slotName" : slotName
                    })
                    if slot_serializer.is_valid():
                        if slot_serializer.save():
                            return JsonResponse({
                                "message": "Successfully Slots added"
                            }, status=200)
                        else:
                            return JsonResponse({
                                "message": "failed"
                            }, status=400)

                    else:
                        return JsonResponse({
                            "message": "val"
                        }, status=status.HTTP_400_BAD_REQUEST)

                else:
                    return JsonResponse({
                        "message": "nauthsuper"
                    }, status=status.HTTP_401_UNAUTHORIZED)


            except Token.DoesNotExist:
                return JsonResponse({
                    "message": "Invalid token"
                }, status=status.HTTP_401_UNAUTHORIZED)

        else:
            return JsonResponse({
                "message": "naaauth"
            }, status=status.HTTP_401_UNAUTHORIZED)

    if request.method == 'GET':

        slots = bookingSlot.objects.all()
        data = []
        for slot in slots:
            slots_data={
                'id' : slot.id,
                'slotName' : slot.slotName
            }
            data.append(slots_data)

        return JsonResponse({
            "slots": data
        },safe=False, status=status.HTTP_200_OK)


    if request.method == 'PUT':
        data = JSONParser().parse(request)
        slot_id = data.get("id")
        slotName = data.get("slotName")
        provided_token = request.META.get('HTTP_AUTHORIZATION')
        if provided_token and provided_token.startswith('Bearer '):
            token_key = provided_token.split(' ')[1]
            try:
                token = Token.objects.get(key=token_key)
                user = token.user
                if(user.is_superuser == 1):
                    slot = bookingSlot.objects.filter(id=slot_id).first()
                    slot_serializer = BookingSerializer(slot,data=data)
                    if slot_serializer.is_valid():
                        slot_serializer.save()
                        return JsonResponse({
                            "message": "suc"
                        }, status=status.HTTP_200_OK)

                    else:
                        return JsonResponse({
                            "message": data
                        }, status=status.HTTP_400_BAD_REQUEST)

                else:
                    return JsonResponse({
                        "message": "nauthsuper"
                    }, status=status.HTTP_401_UNAUTHORIZED)


            except Token.DoesNotExist:
                return JsonResponse({
                    "message": "Invalid token"
                }, status=status.HTTP_401_UNAUTHORIZED)

        else:
            return JsonResponse({
                "message": "naaauth"
            }, status=status.HTTP_401_UNAUTHORIZED)




