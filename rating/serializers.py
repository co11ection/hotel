from rest_framework import serializers
from .models import Review

class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.email')
    room = serializers.ReadOnlyField(source ='room.room')

    class Meta:
        model = Review
        fields = '__all__'

    def create(self, validated_data):
        request = self.context.get('request')
        user = request.user
        room = self.context.get('room')
        validated_data['user'] = user
        validated_data['room'] = room
        return super().create(validated_data)