from .factories import OrderFactory
from ..serializers import OrderSerializer
from .. import Order
from ...base.tests import BaseTestCase
from ...account.tests.factories import AccountFactory
from ...position import Position

class TestOrderSerializers(BaseTestCase):
    def test_data(self):
        """
        Test that all the data is present in the serializer
        """
        order = OrderFactory()
        serializer = OrderSerializer(order, False)

        for item in (
            'symbol', 'qty', 'stop_price', 
            'side', 'order_type', 'status', 
            'filled_at', 'cancelled_at',
        ):
            assert item in serializer.to_representation().keys()

        for method in serializer.custom_fields:
            try:
                assert getattr(order, method)() == serializer.to_representation()[method]
            except TypeError:
                assert getattr(order, method).id == serializer.to_representation()[method]

    def test_is_valid(self):
        """
        Test that validation is right
        """
        account = AccountFactory()

        # Test with account id
        data = {
            'symbol': 'TSLA',
            'qty': 1,
            'side': Position.LONG,
            'order_type': Order.MARKET,
            'account': account.id
        }
        serializer = OrderSerializer(data, True)

        assert type(serializer.to_representation()['id']) == int

        # Test with account instance
        data['account'] = account
        serializer = OrderSerializer(data, True)

        assert type(serializer.to_representation()['id']) == int

        # Test with invalid type
        data['order_type'] = 'blabla'
        serializer = OrderSerializer(data, True)

        assert serializer.errors[0] == {
            'field': 'order_type',
            'error': f'The chosen order_type is incorrect.'
        }
        assert type(serializer.instance) == dict

        # Test with invalid side
        data['side'] = 'blabla'
        serializer = OrderSerializer(data, True)

        assert serializer.errors[0] == {
            'field': 'side',
            'error': f'The chosen side is incorrect.'
        }
        assert type(serializer.instance) == dict