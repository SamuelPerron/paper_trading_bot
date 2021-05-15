from ...base.tests import BaseTestCase
from ..models import Position


class TestPositionModels(BaseTestCase):
    def test_cost_basis(self):
        """
        Checks that cost_basis returns correct value
        """
        raise NotImplementedError()

    def test_market_value(self):
        """
        Checks that market_value returns correct value
        """
        raise NotImplementedError()

    def test_unrealized_pl(self):
        """
        Checks that unrealized_pl returns correct value
        """
        raise NotImplementedError()

    def test_change_today(self):
        """
        Checks that change_today returns correct value
        """
        raise NotImplementedError()

    def test_unrealized_intraday_pl(self):
        """
        Checks that unrealized_intraday_pl returns correct value
        """
        raise NotImplementedError()

    def test_unrealized_intraday_plpc(self):
        """
        Checks that unrealized_intraday_plpc returns correct value
        """
        raise NotImplementedError()

    def test_current_price(self):
        """
        Checks that current_price returns a number
        """
        raise NotImplementedError()

    def test_last_day_price(self):
        """
        Checks that last_day_price returns a number
        """
        raise NotImplementedError()