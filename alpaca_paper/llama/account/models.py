from .. import db
from ..base import BaseDBModel
from ..base.utils import clock
from datetime import datetime, timedelta


association_table_account_historical_equities = db.Table(
    'association_account_historical_equities', db.Model.metadata,
        db.Column('account_id', db.Integer, db.ForeignKey('accounts.id')),
        db.Column('historical_equity_id', db.Integer, db.ForeignKey(
            'historical_equities.id'))
)

association_table_account_positions = db.Table(
    'association_account_positions', db.Model.metadata,
        db.Column('account_id', db.Integer, db.ForeignKey('accounts.id')),
        db.Column('position_id', db.Integer, db.ForeignKey(
            'positions.id'))
)

association_table_account_orders = db.Table(
    'association_account_orders', db.Model.metadata,
        db.Column('account_id', db.Integer, db.ForeignKey('accounts.id')),
        db.Column('order_id', db.Integer, db.ForeignKey(
            'orders.id'))
)


class Account(db.Model, BaseDBModel):
    __tablename__ = 'accounts'

    cash = db.Column(db.Float, default=0)

    historical_equities = db.relationship(
        'HistoricalEquity', 
        secondary=association_table_account_historical_equities)
    positions = db.relationship(
        'Position', 
        secondary=association_table_account_positions)
    orders = db.relationship(
        'Order', 
        secondary=association_table_account_orders)

    def equity(self):
        """
        Total value of cash + holding positions
        """
        equity = self.cash + sum((p.market_value() for p in self.positions))

        historical = HistoricalEquity(
            timestamp=datetime.now(),
            equity=equity
        )
        historical.save_to_db()
        self.historical_equities.append(historical)
        self.save_to_db()

        return equity

    def last_equity(self):
        """
        Equity as of previous trading day at 16:00:00 ET
        """
        grace_period = 5

        last_close = datetime.strptime(clock()['last_close'], '%Y-%m-%dT%H:%M')
        start_grace = last_close - timedelta(minutes=grace_period)
        finish_grace = last_close + timedelta(minutes=grace_period)

        for h in self.historical_equities:
            if h.timestamp >= start_grace and h.timestamp <= finish_grace:
                return h.equity
        
        return None

    def buying_power(self):
        """
        Current available $ buying power
        """
        # Since orders are filled instantly for now, buying power
        # will always equal cash on hand. 
        # TODO: Substract cash locked up in open orders
        return self.cash

    def json(self):
        return {
            'id': self.id,
            'cash': self.cash,
            'equity': self.equity(),
            'last_equity': self.last_equity(),
            'buying_power': self.buying_power(),
        }


class HistoricalEquity(db.Model, BaseDBModel):
    __tablename__ = 'historical_equities'

    timestamp = db.Column(db.DateTime)
    equity = db.Column(db.Float)
