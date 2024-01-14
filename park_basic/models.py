from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator


class reserver(models.Model):
    carNo_validator = RegexValidator(
        regex=r'^([a-zA-Z]{1,3}|([0-9]{1,3}))-[0-9]{4}$',
        message='Enter a valid car registration number.'
    )

    phnNo_validator = RegexValidator(
        regex=r'^(?:7|0|(?:\+94))[0-9]{9,10}$',
        message='Enter a valid Sri Lankan phone number.'
    )
    carNo = models.CharField(validators=[carNo_validator], max_length=20)
    phnNo = models.CharField(validators=[phnNo_validator],max_length =12)
    userId = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reservations')


class bookingSlot(models.Model):
    slotName = models.CharField(max_length=20)


class bookingTime(models.Model):
    bookingTime = models.CharField(max_length=7);


class booking(models.Model):
    Date = models.DateField()
    Time = models.TimeField()
    reserverId = models.ForeignKey(reserver, on_delete=models.CASCADE)
    timeId = models.ForeignKey(bookingTime, on_delete=models.CASCADE)
    slotId = models.ForeignKey(bookingSlot, on_delete=models.CASCADE)


