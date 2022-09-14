from rest_framework import generics, permissions, response, views
from . import serializers
from .models import Booking
from rest_framework.views import APIView
from rest_framework.response import Response
from datetime import date
# Create your views here.

class CreateBookingView(generics.CreateAPIView):
    serializer_class = serializers.BookingSerializer
    permission_classes= (permissions.IsAuthenticated,)

class UserBookingList(views.APIView):
    permission_classes=(permissions.IsAuthenticated,)

    def get(self, request):
        user = request.user
        orders = user.orders.all()
        serializer = serializers.BookingSerializer(orders, many=True).data
        return response.Response(serializer, status=200)

class UpdateBookingStatusView(views.APIView):
    permission_classes = (permissions.IsAdminUser,)

    
    def patch(self, request, pk):
        status = request.data['status']
        if status not in ['in_process', 'closed']:
            return response.Response('invalid status', status=400)
        order = Booking.objects.get(pk=pk)
        order.status=status
        order.save()
        serializer = serializers.BookingSerializer(order).data
        return response.Response(serializer, status=206)


