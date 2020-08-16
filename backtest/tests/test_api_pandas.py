import pytest
import pandas
from ..api_pandas import ApiPandas

class TestApiPandas:
    @pytest.fixture
    def api(self):
        return ApiPandas('CTC-A.TO')

    def test_df(self, api):
        assert api.symbol == 'CTC-A.TO'
        assert type(api.df) == pandas.core.frame.DataFrame

    def test_indicators(self, api):
        assert api.df.loc['2019-05-30']['RSI'] == 20.000115773626433
        assert api.df.loc['2019-05-30']['5d_ma'] == 131.84843140000027
        assert api.df.loc['2019-05-30']['10d_ma'] == 132.95210269999987
        assert api.df.loc['2019-05-30']['50d_ma'] == 138.56248019999998
        assert api.df.loc['2019-05-30']['200d_ma'] == 141.17903708500023
