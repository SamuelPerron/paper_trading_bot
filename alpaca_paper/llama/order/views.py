from flask import Blueprint, abort, request
from .. import app
from .models import Order
from .serializers import OrderSerializer
from ..base.responses import ListHttpResponse, ErrorHttpResponse, DetailsHttpResponse

orders_blueprint = Blueprint('orders', __name__)

@orders_blueprint.route('/', methods=('GET', 'POST',))
def orders():
    if request.method == 'GET':
        orders = Order.query.all()
        response = ListHttpResponse(orders, OrderSerializer, request)
        return response.json()

    serializer = OrderSerializer(request.json, True)
    if len(serializer.errors) == 0:
        return DetailsHttpResponse(serializer.instance, OrderSerializer, request).json()
    else:
        return ErrorHttpResponse(serializer.errors).json()
    