from ...base.tests import BaseTestCase
from .factories import OrderFactory


class TestOrderModels(BaseTestCase):
    def test_create_order(self):
        # Creating an order should add it to the account orders
        # and freeze the funds necessary for the execution
        pass

    def test_create_short_order_without_holding_symbol(self):
        # This should fail for now
        pass

    def test_fill_long_order(self):
        # This should remove the funds from the cash balance of the account
        # and create the right position 
        pass

    def test_fill_short_order(self):
        # This should add the gain of the sale to the 
        # cash balance of the account and close the right position
        pass

    def test_cancel_order(self):
        # This should cancel the order, any subsequent attempts to
        # fill the order should fail
        pass

    def test_stop_loss(self):
        # The order should fill when the stop price is reached
        pass