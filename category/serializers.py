from rest_framework import serializers
from .models import Category
from rooms.serializers import RoomListSerializer

class CategoryListSerializer(serializers.ModelSerializer):
    slug = serializers.ReadOnlyField()
    class Meta:
        model = Category
        fields = '__all__'
    
    def to_representation(self, instance):
        repr = super().to_representation(instance)
        repr['rooms'] = RoomListSerializer(instance.rooms.all(), many = True)
        return repr

class CategoryDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__' 




