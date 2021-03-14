from .. import db, BaseDBModel


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


class Account(db.Model, BaseDBModel):
    __tablename__ = 'accounts'

    cash = db.Column(db.Float, default=0)

    historical_equities = db.relationship(
        'HistoricalEquity', 
        secondary=association_table_account_historical_equities)
    positions = db.relationship(
        'Position', 
        secondary=association_table_account_positions)

    def equity(self):
        """
        Total value of cash + holding positions
        """
        pass

    def last_equity(self):
        """
        Equity as of previous trading day at 16:00:00 ET
        """
        pass

    def buying_power(self):
        """
        Current available $ buying power
        """
        pass

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
