from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework import permissions
from . import serializers
from .models import Category
from rest_framework import permissions
from .permissions import IsAdminOrReadOnly
from rest_framework.decorators import action
# Create your views here.


class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    permission_classes =[IsAdminOrReadOnly]
    serializer_class = serializers.CategoryListSerializer
    # def get_serializer_class(self):
    #     if self.action == 'list':
    #         return serializers.CategoryListSerializer
    #     return serializers.CategoryDetailSerializer

