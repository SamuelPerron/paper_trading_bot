from .. import db
from ..base import BaseDBModel
from ..base.utils import alpaca, bars
from sqlalchemy_utils.types.choice import ChoiceType
from sqlalchemy.orm import relationship


class Position(db.Model, BaseDBModel):
    __tablename__ = 'positions'

    LONG = 'long'
    SHORT = 'short'
    SIDES = (
        (LONG, 'Long'),
        (SHORT, 'Short'),
    )

    account_id = db.Column(
        db.Integer, 
        db.ForeignKey('accounts.id'), 
        nullable=False
    )
    symbol = db.Column(db.String)
    qty = db.Column(db.Integer)
    side = db.Column(ChoiceType(SIDES))
    entry_price = db.Column(db.Float)
    closed = db.Column(db.Boolean, default=False)

    account = relationship(
        'Account', 
        foreign_keys='Position.account_id', 
        backref='positions'
    )

    def cost_basis(self):
        """
        Total cost basis in dollar
        """
        return self.qty * self.entry_price

    def market_value(self):
        """
        Total dollar amount of the position
        """
        return self.qty * self.current_price()

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
        cost_basis = self.cost_basis()
        return (self.unrealized_intraday_pl() - cost_basis) / cost_basis

    def current_price(self):
        """
        Current asset price per share
        """
        return bars(
            [self.symbol], 
            'minute', 
            1
        )[self.symbol][0]['c']

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

