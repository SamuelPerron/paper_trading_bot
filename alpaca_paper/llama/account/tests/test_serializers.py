from .factories import AccountFactory
from ..serializers import AccountSerializer
from ...base.tests import BaseTestCase

class TestAccountSerializers(BaseTestCase):
    def test_data(self):
        """
        Test that all the data is present in the serializer
        """
        account = AccountFactory()
        serializer = AccountSerializer(account, False)

        for item in ('cash', 'equity', 'last_equity', 'buying_power'):
            assert item in serializer.to_representation().keys()

        for method in serializer.custom_fields:
            assert getattr(account, method)() == serializer.to_representation()[method]