import uuid
from django.db import models
from customers.models import Customer


class Order(models.Model):
    """
    Represents an order placed by a customer.

    Attributes:
        id (UUIDField): Unique identifier for the order.
        customer (ForeignKey): Reference to the customer placing the order.
        item_name (CharField): Name of the item ordered.
        quantity (IntegerField): Quantity of the item ordered.
        amount (DecimalField): Total cost of the order.
        order_date (DateTimeField): Timestamp when the order was placed.
        updated_at (DateTimeField): Timestamp when the order was last updated.
        status (CharField): Status of the order (Pending, Completed, or Cancelled).
    """

    STATUS_CHOICES = [
        ("Pending", "Pending"),
        ("Completed", "Completed"),
        ("Cancelled", "Cancelled"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    customer = models.ForeignKey(
        Customer, on_delete=models.CASCADE, related_name="orders"
    )
    item_name = models.CharField(max_length=255)
    quantity = models.IntegerField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    order_date = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="Pending")

    def __str__(self) -> str:
        return f"{self.item_name} - {self.customer.name}"
