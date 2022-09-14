from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter
from rest_framework import permissions, response,generics
from . import serializers
from .models import Rooms, Comment, Like, Favorites
from rest_framework.decorators import action
from rating.serializers import ReviewSerializer
from .permissions import IsAuthor
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination
# Create your views here.
class StandartPagination(PageNumberPagination):
    page_size = 10
    page_query_param = 'page'
    max_page_size = 1000

class RoomViewSet(ModelViewSet):
    queryset = Rooms.objects.all()
    filterset_fields = (DjangoFilterBackend, SearchFilter)
    filterset_fields = ('category','price')
    search_fields = ('room')
    pagination_class = StandartPagination
    
    def perform_create(self, serializer):
        serializer.save()

    def get_serializer_class(self):
        if self.action == 'list':
            return serializers.RoomListSerializer
        else:
            return serializers.RoomDetailSerializer

    
    
    def get_permissions(self):
        if self.action in ('add_to_liked', 'remove_from_liked', 'favorite_action','get_likes'):
            return [permissions.IsAuthenticated(),]
        elif self.action in ('update', 'partial_update', 'destroy', 'create'):
            return [permissions.IsAdminUser(),]
        else:
            return [permissions.AllowAny(),]
    
    @action(['GET', 'POST'], detail=True)
    def reviews(self, request, pk=None):
        room = self.get_object()
        if request.method=='GET':
            reviews = room.reviews.all()
            serializer = ReviewSerializer(reviews, many=True).data
            return response.Response(serializer, status=200)
        data = request.data
        serializer = ReviewSerializer(data=data, context={'request':request, 'room':room})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return response.Response(serializer.data, status= 201)
    
    @action(['GET'], detail=True)
    def comments(self, request, pk):
        room = self.get_object()
        comments = room.comments.all()
        serializer = serializers.CommentSerializer(comments, many=True)
        return response.Response(serializer.data, status=200)
    
    # api/v1/posts/<id>/add_to_liked/
    @action(['POST'], detail=True)
    def add_to_liked(self, request, pk):
        room = self.get_object()
        if request.user.liked.filter(room=room).exists():
            # request.user.liked.filter(post=post).delete()
            return response.Response('Вы уже лайкали этот пост!', status=400)
        Like.objects.create(room=room, user=request.user)
        return response.Response('Вы поставили лайк!', status=201)
    
    # api/v1/posts/<id>/remove_from_liked/
    @action(['POST'], detail=True)
    def remove_from_liked(self, request, pk):
        room = self.get_object()
        if not request.user.liked.filter(room=room).exists():
            return response.Response('Вы не лайкали этот пост!', status=400)
        request.user.liked.filter(room=room).delete()
        return response.Response('Ваш лайк удален!', status=204)

    # api/v1/posts/<id>/get_likes/
    @action(['GET'], detail=True)
    def get_likes(self, request, pk):
        room = self.get_object()
        likes = room.likes.all()
        serializer = serializers.LikeSerializer(likes, many=True)
        return response.Response(serializer.data, status=200)
    
    # api/v1/posts/<id>/favorite_action/
    @action(['POST'], detail=True)
    def favorite_action(self, request, pk):
        room = self.get_object()
        if request.user.favorites.filter(room=room).exists():
            request.user.favorites.filter(room=room).delete()
            return response.Response('Убрали из избранных!', status=204)
        Favorites.objects.create(room=room, user=request.user)
        return response.Response('Добавлено в избранное!', status=201)


class CommentListCreateView(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = serializers.CommentSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class CommentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = serializers.CommentSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsAuthor)
