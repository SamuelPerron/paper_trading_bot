from .. import db
from ..base import BaseDBModel
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
