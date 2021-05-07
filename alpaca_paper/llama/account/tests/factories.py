import factory
from faker import Faker
from ... import db
from .. import Account

fake = Faker()

class AccountFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Account
        sqlalchemy_session = db.session
        sqlalchemy_session_persistence = 'commit'

    cash = factory.Faker('pyfloat', positive=True)

    