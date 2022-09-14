from django.urls import path, include
from . import views

urlpatterns = [
    path('comments/', views.CommentListCreateView.as_view()),
    path('comments/<int:pk>/', views.CommentDetailView.as_view()),
]