from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import Customer
from .serializers import CustomerSerializer
from .services.customer_service import CustomerService


class CustomerListCreateView(generics.ListCreateAPIView):
    """Handles listing and creating customers."""

    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        """
        Calls CustomerService to create a new customer.
        """
        serializer.instance = CustomerService.create_customer(serializer.validated_data)


class CustomerDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Handles retrieving, updating, and deleting customers."""

    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [IsAuthenticated]

    def perform_update(self, serializer):
        """
        Calls CustomerService to update a customer.
        """
        serializer.instance = CustomerService.update_customer(
            self.get_object(), serializer.validated_data
        )

    def perform_destroy(self, instance):
        """
        Calls CustomerService to delete a customer.
        """
        CustomerService.delete_customer(instance)
