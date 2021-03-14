from .. import db, BaseDBModel
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

    def market_value(self):
        """
        Total dollar amount of the position
        """
        pass

    def unrealized_pl(self):
        """
        Unrealized profit/loss in dollars
        """
        pass

    def unrealized_plpc(self):
        """
        Unrealized profit/loss percent (by a factor of 1)
        """
        pass

    def unrealized_intraday_pl(self):
        """
        Unrealized profit/loss in dollars for the day
        """
        pass

    def unrealized_intraday_plpc(self):
        """
        Unrealized profit/loss percent (by a factor of 1)
        """
        pass

    def current_price(self):
        """
        Current asset price per share
        """
        pass

    def lastday_price(self):
        """
        Last day’s asset price per share based on the closing value of the last trading day
        """
        pass

    def change_today(self):
        """
        Percent change from last day price (by a factor of 1)
        """
        pass

    def json(self):
        return {
            'id': self.id,
            'symbol': self.symbol,
            'qty': self.qty,
            'side': self.side,
            'market_value': self.market_value(),
            'unrealized_pl': self.unrealized_pl(),
            'unrealized_plpc': self.unrealized_plpc(),
            'unrealized_intraday_pl': self.unrealized_intraday_pl(),
            'unrealized_intraday_plpc': self.unrealized_intraday_plpc(),
            'current_price': self.current_price(),
            'lastday_price': self.lastday_price(),
            'change_today': self.change_today(),
        }

