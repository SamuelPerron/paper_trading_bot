import pytest
from alpaca_paper import Alpaca


@pytest.fixture
def alpaca():
    return Alpaca()

def test_alpaca_class(alpaca):
    assert 'Alpaca <id: ' in str(alpaca)

def test_api(alpaca):
    request = alpaca.api('get', 'orders')
    assert request.url == f'{alpaca.base_url}/orders'

def test_api_params(alpaca):
    request = alpaca.api('get', 'orders', {'status': 'open'})
    assert request.url == f'{alpaca.base_url}/orders?status=open'

def test_account(alpaca):
    account = alpaca.account()
    assert 'id' in account.keys()

def test_orders(alpaca):
    orders = alpaca.orders()
    assert isinstance(orders, (list,))

def test_order(alpaca):
    order = alpaca.orders(id='id_of_order')
    assert isinstance(order, (dict,))

def test_order_and_filter(alpaca):
    with pytest.raises(Exception) as e:
        alpaca.orders(id='id_of_order', filter={'sttaus': 'open'})

def test_orders_random_filter(alpaca):
    with pytest.raises(Exception) as e:
        alpaca.orders(filter={'random': 'impossible'})

def test_new_order_required(alpaca):
    details = {'symbol': 'TSLA',}
    with pytest.raises(Exception) as e:
        alpaca.new_order(details)

def test_new_order_required_limit_price(alpaca):
    details = {
        'symbol': 'TSLA', 'qty': 4, 'side': 'buy', 'type': 'limit'
    }
    with pytest.raises(Exception) as e:
        alpaca.new_order(details)

def test_new_order_required_stop_price(alpaca):
    details = {
        'symbol': 'TSLA', 'qty': 4, 'side': 'buy', 'type': 'stop'
    }
    with pytest.raises(Exception) as e:
        alpaca.new_order(details)

def test_clock(alpaca):
    assert 'timestamp' in alpaca.clock().keys()

def test_positions(alpaca):
    positions = alpaca.positions()
    assert isinstance(positions, (list,))

def test_position(alpaca):
    position = alpaca.positions(symbol='TSLA')
    assert isinstance(position, (dict,))