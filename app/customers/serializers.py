from .models import Customer
from rest_framework import serializers


class CustomerSerializer(serializers.ModelSerializer):
    """
    Serializer for the Customer model.
    Converts model instances into JSON format.
    """

    class Meta:
        model = Customer
        fields = "__all__"
