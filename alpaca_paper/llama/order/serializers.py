from ..base.serializers import ModelSerializer
from .models import Order


class OrderSerializer(ModelSerializer):
    model = Order
    fields = '__all__'
