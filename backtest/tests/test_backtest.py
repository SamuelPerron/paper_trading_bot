import pytest

from ..backtest import Backtest

class TestBacktest:
    @pytest.fixture
    def backtest(self):
        return Backtest('CTC-A.TO', 1)

    def test_strategy_loaded_ok(self, backtest):
        assert backtest.position_size == 0.15
