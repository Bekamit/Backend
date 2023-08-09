from django.contrib import admin
from account.models import CustomUser
from hotel.models import Hotel, RoomType, Equipment, Room, Amenity, Booking

admin.site.register(CustomUser)
admin.site.register(Hotel)
admin.site.register(RoomType)
admin.site.register(Equipment)
admin.site.register(Room)
admin.site.register(Amenity)
admin.site.register(Booking)