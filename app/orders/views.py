from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import Order
from .serializers import OrderSerializer
from .services.order_service import OrderService


class OrderListCreateView(generics.ListCreateAPIView):
    """Handles listing and creating orders."""

    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        """
        Calls OrderService to create a new order.
        """
        serializer.instance = OrderService.create_order(serializer.validated_data)


class OrderDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Handles retrieving, updating, and deleting orders."""

    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def perform_update(self, serializer):
        """
        Calls OrderService to update an order.
        """
        serializer.instance = OrderService.update_order(
            self.get_object(), serializer.validated_data
        )

    def perform_destroy(self, instance):
        """
        Calls OrderService to delete an order.
        """
        OrderService.delete_order(instance)
