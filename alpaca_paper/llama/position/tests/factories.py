import factory
import factory.fuzzy as fuzzy
from faker import Faker
from ... import db
from .. import Position
from ...account.tests.factories import AccountFactory
from ...order.tests.factories import STOCK_SYMBOLS

fake = Faker()

class PositionFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Position
        sqlalchemy_session = db.session
        sqlalchemy_session_persistence = 'commit'

    account = factory.SubFactory(AccountFactory)
    symbol = fuzzy.FuzzyChoice(STOCK_SYMBOLS)
    qty = fake.random_digit_not_null()
    side = fuzzy.FuzzyChoice(
        Position.SIDES, getter=lambda c: c[0]
    )
    entry_price = fake.pyfloat(positive=True, min_value=0.01, max_value=1200)

    class Params:
        closed = factory.Trait(
            closed=True
        )

    