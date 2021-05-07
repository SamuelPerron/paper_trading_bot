from .. import db
from ..base import BaseDBModel
from ..base.utils import bars
from ..position import Position
from sqlalchemy_utils.types.choice import ChoiceType
from sqlalchemy.orm import relationship
from datetime import datetime


NOT_HOLDING_POSITION = 'Not holding position.'
INSUFFICIENT_FUNDS = 'Insufficient funds.'

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
    REJECTED = 'rejected'
    STATUSES = (
        (NEW, 'New'),
        (FILLED, 'Filled'),
        (CANCELLED, 'Cancelled'),
        (REJECTED, 'Rejected'),
    )

    account_id = db.Column(
        db.Integer, 
        db.ForeignKey('accounts.id'), 
        nullable=False
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
    rejected_cause = db.Column(db.String)

    account = relationship(
        'Account', 
        foreign_keys='Order.account_id', 
        backref='orders'
    )

    def get_public_fields():
        return BaseDBModel.get_public_fields() + (
            'symbol', 'qty', 'stop_price', 
            'side', 'order_type', 'status', 
            'filled_at', 'cancelled_at',
        )

    def fill(self):
        if self.status == Order.CANCELLED:
            return False

        if self.side == Position.SHORT:
            if self.symbol not in (p.symbol for p in self.account.positions):
                self.status = Order.REJECTED
                self.rejected_cause = NOT_HOLDING_POSITION
                self.save_to_db()
                return False

            current_price = self.get_current_price()
            position = self.get_related_position()

            if position.qty < self.qty:
                self.status = Order.REJECTED
                self.rejected_cause = NOT_HOLDING_POSITION
                self.save_to_db()
                return False

            position.closed = True
            position.save_to_db()

            self.account.cash += (current_price * self.qty)
            self.status = Order.FILLED
            self.filled_at = datetime.now()
            self.filled_price = current_price
            self.save_to_db()

            if position.qty > self.qty:
                new_position = Position(
                    account=self.account,
                    symbol=self.symbol,
                    qty=position.qty - self.qty,
                    side=Position.LONG,
                    entry_price=position.entry_price
                )
                new_position.save_to_db()

            return True

        if self.side == Position.LONG:
            current_price = self.get_current_price()
            account_equity = self.account.cash + self.needed_funds
            total_price = current_price * self.qty

            if account_equity < total_price:
                self.status = Order.REJECTED
                self.rejected_cause = INSUFFICIENT_FUNDS
                self.save_to_db()
                return False
 
            self.account.cash += self.needed_funds
            self.account.cash -= total_price
            self.account.save_to_db()
            
            position = Position(
                account=self.account,
                symbol=self.symbol,
                qty=self.qty,
                side=self.side,
                entry_price=current_price
            )
            position.save_to_db()

            self.filled_price = current_price
            self.filled_at = datetime.now()
            self.status = Order.FILLED
            self.save_to_db()
            return True

    def cancel(self):
        if self.status != Order.NEW:
            return False

        self.status = Order.CANCELLED
        self.account.cash += self.needed_funds
        self.save_to_db()
        self.account.save_to_db()
        return True

    def get_related_position(self):
        return Position.query.filter_by(
                account=self.account,
                symbol=self.symbol,
                side=Position.LONG,
                closed=False
            ).first()

    def get_current_price(self):
        return bars(
            [self.symbol], 
            'minute', 
            1
        )[self.symbol][0]['c']

    def save_to_db(self):
        if self.id is None and self.side == Position.LONG:
            current_price = self.get_current_price()

            self.needed_funds = current_price * self.qty
            self.account.cash -= self.needed_funds
            self.account.save_to_db()

        super().save_to_db()

    def __str__(self):
        return f'<Order [{self.symbol}] {self.side} | {self.status}>'
