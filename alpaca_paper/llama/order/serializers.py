from ..base.serializers import ModelSerializer
from ..base.utils import get_choices
from .models import Order
from ..position import Position


class OrderSerializer(ModelSerializer):
    model = Order
    fields = '__all__'

    def is_valid(self, final_instance):
        super().is_valid(final_instance)

        to_validate = (
            ('side', get_choices(Position.SIDES)),
            ('order_type', get_choices(Order.TYPES)),
        )

        for field, choices in to_validate:
            if self.instance[field] not in choices:
                self.errors.append({
                    'field': field,
                    'error': f'The chosen {field} is incorrect.'
                })
