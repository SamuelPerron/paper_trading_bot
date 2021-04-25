from ..base.serializers import ModelSerializer
from .models import Account


class AccountSerializer(ModelSerializer):
    model = Account
    fields = '__all__'
    custom_fields = ('equity', 'last_equity', 'buying_power')

    def get_equity(self):
        return getattr(self.instance, 'equity')()

    def get_last_equity(self):
        return getattr(self.instance, 'last_equity')()

    def get_buying_power(self):
        return getattr(self.instance, 'buying_power')()
