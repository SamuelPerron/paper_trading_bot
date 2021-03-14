from .. import db
from ..base import BaseDBModel
from ..base.utils import alpaca, bars
from sqlalchemy_utils.types.choice import ChoiceType
import enum


class PositionSides(enum.Enum):
    buy = 1
    sell = 2

class Position(db.Model, BaseDBModel):
    __tablename__ = 'positions'

    SIDES = (
        ('buy', 'Buy'),
        ('sell', 'Sell'),
    )

    symbol = db.Column(db.String)
    qty = db.Column(db.Integer)
    side = db.Column(ChoiceType(SIDES))
    entry_price = db.Column(db.Float)

    def cost_basis(self):
        """
        Total cost basis in dollar
        """
        return self.qty * self.entry_price

    def market_value(self):
        """
        Total dollar amount of the position
        """
        return self.cost_basis() + (self.qty + self.current_price())

    def unrealized_pl(self):
        """
        Unrealized profit/loss in dollars
        """
        return self.market_value() - self.cost_basis()

    def unrealized_plpc(self):
        """
        Unrealized profit/loss percent
        """
        return self.unrealized_pl() / self.cost_basis()

    def change_today(self):
        """
        Percent change from last day price
        """
        return self.current_price() - self.lastday_price()

    def unrealized_intraday_pl(self):
        """
        Unrealized profit/loss in dollars for the day
        """
        return self.change_today() * self.qty

    def unrealized_intraday_plpc(self):
        """
        Unrealized profit/loss percent for the day
        """
        (self.unrealized_intraday_pl() - self.cost_basis()) / self.cost_basis()

    def current_price(self):
        """
        Current asset price per share
        """
        response = alpaca('get', f'last_quote/stocks/{self.symbol}')
        if response.status_code == 200:
            return response.json()['last']['askprice']
        return None

    def lastday_price(self):
        """
        Last day’s asset price per share based on the closing value of the last trading day
        """
        data = bars((self.symbol,), 'day', limit=1)[self.symbol][0]
        return self.current_price() - data['c']


    def json(self):
        return {
            'id': self.id,
            'symbol': self.symbol,
            'qty': self.qty,
            'side': self.side,
            'cost_basis': self.cost_basis(),
            'market_value': self.market_value(),
            'unrealized_pl': self.unrealized_pl(),
            'unrealized_plpc': self.unrealized_plpc(),
            'unrealized_intraday_pl': self.unrealized_intraday_pl(),
            'unrealized_intraday_plpc': self.unrealized_intraday_plpc(),
            'current_price': self.current_price(),
            'lastday_price': self.lastday_price(),
            'change_today': self.change_today(),
        }

