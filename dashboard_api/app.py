# Python
from datetime import datetime

# Libraries
import alpaca_trade_api as tradeapi
from flask_api import FlaskAPI

# Env variables
from ..dotenv import ALPACA_UID, ALPACA_SECRET, DASHBOARD_API_URL
from ..global_settings import DASHBOARD_API_VERSION, BOT_VERSION


# Settings
app = FlaskAPI(__name__)
broker = tradeapi.REST(ALPACA_UID, ALPACA_SECRET, base_url='https://paper-api.alpaca.markets')
base_url = DASHBOARD_API_URL

# Meta data
metadata = {
    'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
    'timestamp_format': '%Y-%m-%d %H:%M:%S',
    'broker': 'https://alpaca.markets/',
    'broker_type': 'paper',
    'bot_version': BOT_VERSION,
    'dashboard_api_version': DASHBOARD_API_VERSION,
}


# Endpoints
@app.route('/')
def home():
    return {
        'positions': f'{DASHBOARD_API_URL}/positions',
        'orders': f'{DASHBOARD_API_URL}/orders',
        'account': f'{DASHBOARD_API_URL}/account',
        'meta': metadata
    }

@app.route('/positions')
def positions():
    positions = broker.list_positions()
    to_return = {
        'positions': [],
        'meta': metadata
    }

    for position in positions:
        to_return['positions'].append({
            'symbol': position.symbol,
            'market_value': float(position.market_value),
            'entry_price': float(position.avg_entry_price),
            'qty': float(position.qty),
            'current_price': float(position.current_price),
            'lastday_price': float(position.lastday_price),
            'pl_today': float(position.current_price) - float(position.lastday_price),
            'pl_today_prct': float(position.change_today),
            'unrealized_pl': float(position.unrealized_pl),
            'unrealized_pl_prct': float(position.unrealized_plpc),
        })

    return to_return


@app.route('/account')
def account():
    account = broker.get_account()
    cash = float(account.cash)
    account_value = float(account.equity)
    last_day_account_value = float(account.last_equity)
    buying_power = float(account.buying_power)
    total_deposit = 1000.0

    to_return = {
        'account': {
            # Account infos
            'id': account.id,
            'currency': account.currency,
            # Cash infos
            'cash': cash,
            'market_value': account_value - cash,
            'account_value': account_value,
            'last_day_account_value': last_day_account_value,
            'buying_power': buying_power,
            'total_deposit': total_deposit,
            # Stats
            'day_pl': account_value - last_day_account_value,
            'day_pl_prct': (account_value - last_day_account_value) / abs(last_day_account_value),
            'all_time_pl': account_value - total_deposit,
            'all_time_pl_prct': (account_value - total_deposit) / total_deposit,
        },
        'meta': metadata
    }

    return to_return


@app.route('/orders')
def orders():
    orders = broker.list_orders()
    to_return = {
        'orders': [],
        'meta': metadata
    }

    for order in orders:
        to_return['orders'].append({
            'symbol': order.symbol,
            'created_at': order.created_at,
            'submitted_at': order.submitted_at,
            'filled_at': order.filled_at,
            'expired_at': order.expired_at,
            'canceled_at': order.canceled_at,
            'status': order.status,
            'side': order.side,
            'qty': order.qty,
            'filled_avg_price': order.filled_avg_price,
            'limit_price': order.limit_price,
            'stop_price': order.stop_price,
        })

    return to_return
