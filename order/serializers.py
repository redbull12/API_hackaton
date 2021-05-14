from django.contrib.auth import get_user_model, authenticate
from rest_framework import serializers
from order.models import Order
from .utils import send_confirmation_mail

User = get_user_model()



class OrderSerializer(serializers.ModelSerializer):
    # user = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Order
        fields = '__all__'

    def create(self, validated_data):
        order = Order.objects.create(**validated_data)
        order.create_activation_code()
        send_confirmation_mail(order.user, order.activation_code)
        return order
