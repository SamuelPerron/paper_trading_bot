from .factories import PositionFactory
from ..serializers import PositionSerializer
from .. import Position
from ...base.tests import BaseTestCase

class TestPositionSerializers(BaseTestCase):
    def test_data(self):
        """
        Test that all the data is present in the serializer
        """
        position = PositionFactory()
        serializer = PositionSerializer(position, False)

        for item in ('symbol', 'qty', 'side'):
            assert item in serializer.to_representation().keys()

        custom_field = serializer.custom_fields[0]
        assert getattr(position, custom_field)() == serializer.to_representation()[custom_field]
