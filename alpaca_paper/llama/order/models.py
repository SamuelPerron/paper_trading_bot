from .. import db
from ..base import BaseDBModel
from ..base.utils import bars
from ..position import Position
from sqlalchemy_utils.types.choice import ChoiceType

class Order(db.Model, BaseDBModel):
    __tablename__ = 'orders'

    MARKET = 'market'
    STOP = 'stop'
    TYPES = (
        (MARKET, 'Market'),
        (STOP, 'Stop'),
    )

    NEW = 'new'
    FILLED = 'filled'
    CANCELLED = 'cancelled'
    STATUSES = (
        (NEW, 'New'),
        (FILLED, 'Filled'),
        (CANCELLED, 'Cancelled'),
    )

    symbol = db.Column(db.String)
    qty = db.Column(db.Integer)
    needed_funds = db.Column(db.Float)
    filled_price = db.Column(db.Float)
    stop_price = db.Column(db.Float)
    side = db.Column(ChoiceType(Position.SIDES))
    order_type = db.Column(ChoiceType(TYPES))
    status = db.Column(ChoiceType(STATUSES))
    filled_at = db.Column(db.DateTime)
    cancelled_at = db.Column(db.DateTime)

    def get_public_fields():
        return BaseDBModel.get_public_fields() + (
            'symbol', 'qty', 'stop_price', 
            'side', 'order_type', 'status', 
            'filled_at', 'cancelled_at',
        )

    def fill(self):
        pass

    def cancel(self):
        pass

    def save_to_db(self):
        if self.id is None:
            current_price = bars([self.symbol], 'minute', 1)[self.symbol][0]['c']

            self.needed_funds = current_price * self.qty

        super().save_to_db()

    def __str__(self):
        return f'<Order [{self.symbol}] {self.side} | {self.status}>'
