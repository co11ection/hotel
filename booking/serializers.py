from .models import Booking, BookingItem
from rest_framework import serializers

class BookingItemSerializer(serializers.ModelSerializer):
    rooms_room = serializers.ReadOnlyField(source='rooms.room')
    class Meta:
        model = BookingItem
        fields = ('room','arrival_date','departure_date', 'rooms_room')
    
    def to_representation(self, instance):
        repr =  super().to_representation(instance)
        repr.pop('room')
        return repr


class BookingSerializer(serializers.ModelSerializer):
    positions = BookingItemSerializer(write_only=True, many = True)
    status = serializers.CharField(read_only = True)
    user = serializers.ReadOnlyField(source = 'user.email')


    class Meta:
        model = Booking
        fields = ('id', 'user', 'positions','status',)

    def create(self, validated_data):
        rooms = validated_data.pop('positions')
        user = self.context.get('request').user
        booking = Booking.objects.create(user=user, status='booked')

        for rm in rooms:
            room = rm['room']
            arrival_date = rm['arrival_date']
            departure_date = rm['departure_date']
            BookingItem.objects.create(booking=booking, room=room, arrival_date=arrival_date,departure_date=departure_date)
        return booking
    
    def to_representation(self, instance):
        repr = super().to_representation(instance)
        repr['rooms']=BookingItemSerializer(instance.items.all(), many=True).data
        return repr

