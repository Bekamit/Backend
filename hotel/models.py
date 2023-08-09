from django.db import models


# Create your models here.

class AbstractNameDescription(models.Model):
    name = models.CharField(max_length=150)
    description = models.TextField(blank=True)

    objects = models.Manager()

    class Meta:
        abstract = True

class Hotel(AbstractNameDescription):
    address = models.TextField()


class RoomType(AbstractNameDescription):
    pass


class Equipment(AbstractNameDescription):
    pass

class Room(models.Model):
    hotel = models.ForeignKey(
        'Hotel',
            on_delete=models.CASCADE,
            related_name='rooms'
    )
    type = models.ForeignKey(
        'RoomType',
            on_delete=models.CASCADE,
            related_name='rooms'
    )
    equipments = models.ManyToManyField(
        'Equipment',
            related_name='rooms',
            through='Amenity',
            blank=True
    )
    name = models.CharField(max_length=20)
    price = models.DecimalField(max_digits=9, decimal_places=2)
    is_available = models.BooleanField(default=True)

    guests = models.ManyToManyField(
        'account.CustomUser',
        related_name='rooms',
        through='Booking',
        blank=True)

    objects = models.Manager()

class Amenity(models.Model):
    room = models.ForeignKey('Room', on_delete=models.CASCADE, related_name='amenities')
    equipment = models.ForeignKey('Equipment', on_delete=models.CASCADE, related_name='amenities')
    quantity = models.PositiveSmallIntegerField()


    objects = models.Manager()

class Booking(models.Model):
    room = models.ForeignKey('Room', on_delete=models.CASCADE, related_name='bookings')
    guest = models.ForeignKey('account.CustomUser', on_delete=models.CASCADE, related_name='bookings')
    check_in_date = models.DateTimeField()
    check_out_date = models.DateTimeField()


    objects = models.Manager()













