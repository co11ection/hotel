from rest_framework import serializers
from .models import Rooms
from django.db.models import Avg
from .models import Favorites, Like, Comment

class FavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorites
        fields = ('room',)

    def to_representation(self, instance):
        repr=super().to_representation(instance)
       
        repr['room']= RoomListSerializer(instance.room).data
        return repr



class LikeSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source = 'user.email')

    class Meta:
        model = Like
        fields = ('user',)


class CommentSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.email')

    class Meta:
        model = Comment
        fields = ('id', 'body', 'user', 'room')


class RoomListSerializer(serializers.ModelSerializer):
    # user = serializers.ReadOnlyField(source ='user.email')
    class Meta:
        model = Rooms
        fields = ('room', 'price', 'images',)

    def is_liked(self, room):
        user = self.context.get('request').user
        return user.liked.filter(room=room).exists()


    def to_representation(self, instance):
        repr = super().to_representation(instance)
        user = self.context.get('request').user
        if user.is_authenticated:
            repr['is_liked'] = self.is_liked(instance)
        repr['likes_count'] = instance.likes.count()
        return repr

    def to_representation(self, instance):
        repr=super().to_representation(instance)
       
        repr['rating']= instance.reviews.aggregate(Avg('rating'))['rating__avg']
        repr['reviews'] = instance.reviews.count()
        return repr


class RoomDetailSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source ='user.email')
    comments = CommentSerializer(many = True, read_only=True)
    
    class Meta:
        model = Rooms
        fields = '__all__'


    def to_representation(self, instance):
        repr=super().to_representation(instance)
       
        repr['rating']= instance.reviews.aggregate(Avg('rating'))['rating__avg']
        repr['reviews'] = instance.reviews.count()
        return repr

    def is_liked(self, room):
        user = self.context.get('request').user
        return user.liked.filter(room=room).exists()


    def to_representation(self, instance):
        repr = super().to_representation(instance)
        user = self.context.get('request').user
        if user.is_authenticated:
            repr['is_liked'] = self.is_liked(instance)
        repr['likes_count'] = instance.likes.count()
        return repr