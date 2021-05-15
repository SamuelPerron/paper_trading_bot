from ..base.serializers import ModelSerializer
from ..base.utils import get_choices
from .models import Order
from ..position import Position
from ..account import Account


class OrderSerializer(ModelSerializer):
    model = Order
    fields = '__all__'
    custom_fields = ('account',)

    def get_account(self):
        return self.instance.account.id

    def set_account(self, instance, value):
        if type(value) == int:
            instance.account_id = value
            instance.account = Account.query.filter_by(id=value).first()
        elif type(value) == Account:
            instance.account = value

    def valid_account(self, value):
        if type(value) == int:
            account = Account.query.filter_by(id=value).first()
            if not account:
                self.errors.append({
                    'field': 'account',
                    'error': f'Account does not exist.'
                })
        return

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
