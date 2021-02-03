import pytest
from alpaca_paper.screeners import MarketWatch


@pytest.fixture
def mw():
    return MarketWatch()

def test_premarket(mw):
    pre_market = mw.pre_market()
    assert isinstance(pre_market, (dict,))
    assert isinstance(pre_market['gainers'], (list,))
    assert isinstance(pre_market['loosers'], (list,))
    assert isinstance(pre_market['most_actives'], (list,))

def test_vol_to_float():
    assert 221770 == MarketWatch.vol_to_float('221.77K')
    assert 2189000 == MarketWatch.vol_to_float('2.189M')
    assert 3316 == MarketWatch.vol_to_float('3,316')