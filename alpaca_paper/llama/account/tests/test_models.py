from datetime import datetime
from .factories import AccountFactory
from ...base.tests import BaseTestCase
from ...position.tests.factories import PositionFactory
from ...order.tests.factories import OrderFactory

class TestAccountModels(BaseTestCase):
    def test_equity(self):
        """
        Checks that equity returns total cash + total positions value
        It should also create an historical equity
        """
        position = PositionFactory()
        account = position.account
        base_nb_historical_equities = len(account.historical_equities)

        position_value = position.market_value()
        equity = account.equity()
        new_nb_historical_equities = len(account.historical_equities)

        assert equity == account.cash + position_value
        assert new_nb_historical_equities == base_nb_historical_equities + 1

    def test_buying_power(self):
        """
        Checks that buying_power returns total cash - frozen funds in 
        open orders
        """
        account = AccountFactory()
        order = OrderFactory(account=account)
        order.save_to_db()

        cash = account.cash

        assert account.buying_power() == cash

    def test_get_equity_of_date(self):
        """
        Checks that get_equity_of_date returns 
        hisorical equity of specific date
        """
        account = AccountFactory()
        equity = account.equity()

        assert account.get_equity_of_date() == None
        assert account.get_equity_of_date(datetime.now()) == equity