import pytest
from alpaca_paper import Alpaca
from alpaca_paper.big_brain import BigBrain


@pytest.fixture
def alpaca():
    return Alpaca()

def test_bars(alpaca):
    symbols = ['GME', 'AMC']
    bars = alpaca.bars(symbols, big_brain=True)
    assert isinstance(bars, (list,))
    assert isinstance(bars[0], (BigBrain,))
    assert bars[0].symbol in symbols

def test_stats_present(alpaca):
    symbols = ['GME',]
    bars = alpaca.bars(symbols, big_brain=True)
    big_brain = bars[0]
    assert isinstance(big_brain, (BigBrain,))
    assert '5d_ma' in big_brain.df
    assert '200d_ma' in big_brain.df
    assert 'RSI' in big_brain.df
    assert 'MACD' in big_brain.df
    assert 'MACD Signal' in big_brain.df