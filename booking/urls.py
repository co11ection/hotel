from django.urls import path
from . import views

urlpatterns = [
    path('', views.CreateBookingView.as_view()),
    path('own/', views.UserBookingList.as_view()),
    path('<int:pk>/', views.UpdateBookingStatusView.as_view())
]