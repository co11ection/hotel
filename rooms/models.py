from tabnanny import verbose
from django.db import models
from category.models import Category
from django.contrib.auth import get_user_model
# Create your models here.

User = get_user_model()

class Rooms(models.Model):
    room = models.CharField(max_length=30, unique=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='rooms')
    price = models.DecimalField(max_digits=20, decimal_places=2)
    images = models.ImageField(upload_to = 'images/', null = True, blank = True)
    description = models.TextField()

    class Meta:
        ordering = ['room']
        verbose_name = 'rooms'
        verbose_name_plural ='room'
    
    def __str__(self):
        return f'{self.room} -> {self.price}' 


class Comment(models.Model):
    user = models.ForeignKey(User, related_name='comments', on_delete=models.CASCADE)
    room = models.ForeignKey(Rooms, related_name='comments', on_delete=models.CASCADE)
    body = models.TextField()
    created_at = models.DateField(auto_now=True)

    def __str__(self) -> str:
        return f'{self.user} -> {self.room} -> {self.created_at}'


class Like(models.Model):
    room = models.ForeignKey(Rooms, on_delete=models.CASCADE, related_name = 'likes')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='liked')

    class Meta:
        unique_together = ['room', 'user']


class Favorites(models.Model):
    room = models.ForeignKey(Rooms, on_delete=models.CASCADE, related_name='favorites')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorites')

    class Meta:
        unique_together = ['room', 'user']