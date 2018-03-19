from rest_framework import serializers

from .models import Order


class OrderSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False, read_only=False)

    class Meta:
        model = Order
        fields = '__all__'
