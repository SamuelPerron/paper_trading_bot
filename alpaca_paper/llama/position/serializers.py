from ..base.serializers import ModelSerializer
from .models import Position


class PositionSerializer(ModelSerializer):
    model = Position
    fields = '__all__'
    custom_fields = (
        'cost_basis', 'market_value', 'unrealized_pl',
        'unrealized_intraday_pl', 'unrealized_intraday_plpc',
        'current_price', 'lastday_price', 'change_today'
    )