import uuid
from django.db import models


class Customer(models.Model):
    """
    Represents a customer in the system.

    Attributes:
        id (UUIDField): Unique identifier for the customer.
        name (CharField): The customer's name.
        email (EmailField): Unique email for the customer.
        phone_number (CharField): Optional phone number.
        address (TextField): Optional physical address.
        created_at (DateTimeField): Timestamp when the customer was created.
        updated_at (DateTimeField): Timestamp when the customer was last updated.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.name
