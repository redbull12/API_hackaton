from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from order.models import Order
from order.serializers import OrderSerializer

User = get_user_model()


class MakeOrderView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = request.data
        serializer = OrderSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response('Подтвердите заказ по почте', status=201)

class ConfirmOrderView(APIView):
    def get(self, request):
        activation_code = request.query_params.get('u')
        order = get_object_or_404(Order, activation_code=activation_code)
        order.confirmed = True
        order.activation_code = ''
        order.save()
        return Response('Заказ подтвержден', status=200)
