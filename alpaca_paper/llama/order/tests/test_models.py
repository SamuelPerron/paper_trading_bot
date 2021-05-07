import pytest
from unittest.mock import patch
from ...base.tests import BaseTestCase
from ...account.tests.factories import AccountFactory
from ...position import Position
from .factories import OrderFactory


class TestOrderModels(BaseTestCase):
    def test_needed_funds_filled(self):
        # Checks that, when we save an order, the needed_funds field
        # is filled
        order = OrderFactory()
        order.save_to_db()

        assert order.needed_funds is not None

    def test_create_order(self):
        # Creating an order should add it to the account orders
        # and freeze the funds necessary for the execution
        account = AccountFactory()
        original_cash = account.cash

        order = OrderFactory()
        order.save_to_db()
        account.orders.append(order)

        assert order in account.orders
        assert account.cash == original_cash - order.needed_funds

    def test_create_short_order_without_holding_symbol(self):
        # This should cancel the order for now
        account = AccountFactory()

        order = OrderFactory(side=Position.SHORT)
        order.save_to_db()
        account.orders.append(order)

        assert order.fill() == False
        assert order.status == Order.CANCELLED

    def test_fill_long_order(self):
        # This should remove the funds from the cash balance of the account
        # and create the right position 
        account = AccountFactory()
        original_cash = account.cash

        order = OrderFactory(side=Position.LONG)
        order.save_to_db()
        account.orders.append(order)

        assert order.fill() == True
        assert order.status == Order.FILLED
        assert account.cash == original_cash - (order.filled_price * order.qty)
        assert account.positions[0].symbol == order.symbol

    def test_fill_short_order(self):
        # This should add the gain of the sale to the 
        # cash balance of the account and close the right position
        account = AccountFactory()
        long = OrderFactory(side=Position.LONG)
        long.save_to_db()
        account.orders.append(long)
        long.fill()
        original_cash = account.cash

        short = OrderFactory(
            side=Position.SHORT, 
            symbol=long.symbol, 
            qty=long.qty
        )
        short.save_to_db()
        account.orders.append(short)
        
        assert short.fill() == True
        assert short.status == Order.FILLED
        assert account.cash == original_cash + (short.filled_at * short.qty)

    def test_cancel_order(self):
        # This should cancel the order, any subsequent attempts to
        # fill the order should fail. Frozen funds should be recredited.
        account = AccountFactory()
        original_cash = account.cash

        order = OrderFactory()
        order.save_to_db()
        account.orders.append(order)

        order.cancel()

        assert order.status == Order.CANCELLED
        assert order.fill() == False
        assert account.cash == original_cash

    # https://stackoverflow.com/questions/53590758/how-to-mock-function-call-in-flask-restul-resource-method
    def test_stop_loss(self):
        # The order should fill when the stop price is reached
        pass