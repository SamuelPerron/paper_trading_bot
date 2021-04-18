from .. import db
from ..base import BaseDBModel
from ..position import Position
from sqlalchemy_utils.types.choice import ChoiceType

class Order(db.Model, BaseDBModel):
    __tablename__ = 'orders'

    TYPES = (
        ('market', 'Market'),
        ('stop', 'Stop'),
    )

    STATUSES = (
        ('new', 'New'),
        ('filled', 'Filled'),
        ('canceled', 'Canceled'),
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
