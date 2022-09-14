from email.mime import image
from django.db import models
from django.contrib.auth import get_user_model
from rooms.models import Rooms
from django.dispatch import receiver
from django.db.models.signals import post_save
from account.send_email import send_notification
from django.utils.translation import gettext_lazy as _
# Create your models here.

User = get_user_model()

STATUS_CHOISES = (
    ('booked', 'забронировано'),
    ('unbooked','незабронированный')
)

class BookingItem(models.Model):
    booking = models.ForeignKey('Booking', related_name='items', on_delete=models.CASCADE )
    room = models.ForeignKey(Rooms, on_delete=models.CASCADE)
    arrival_date = models.DateField()
    departure_date = models.DateField()

    class Meta:
        unique_together = ['arrival_date', 'departure_date']
    

class Booking(models.Model):
    user = models.ForeignKey(User, related_name='booking', on_delete=models.CASCADE)
    room = models.ManyToManyField(Rooms, through = BookingItem,)
    status = models.CharField(max_length=20, choices=STATUS_CHOISES)

    update_at = models.DateTimeField(auto_now=True)

    # class Meta:
    #     unique_together = ['room', 'user']
    
    def __str__(self) -> str:
        return f'{self.user}'

@receiver(post_save, sender = Booking)
def booking_post_save(sender, instance,*args, **kwargs):
    send_notification(instance.user, instance.id)
