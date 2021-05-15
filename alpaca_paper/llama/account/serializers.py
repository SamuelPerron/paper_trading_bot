from ..base.serializers import ModelSerializer
from .models import Account


class AccountSerializer(ModelSerializer):
    model = Account
    fields = '__all__'
    custom_fields = ('equity', 'last_equity', 'buying_power')
