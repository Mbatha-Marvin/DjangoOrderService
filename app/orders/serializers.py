from .models import Order
from rest_framework import serializers


class OrderSerializer(serializers.ModelSerializer):
    """
    Serializer for the Order model.
    Converts model instances into JSON format.
    """

    class Meta:
        model = Order
        fields = "__all__"
