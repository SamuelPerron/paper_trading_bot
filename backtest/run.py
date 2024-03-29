from backtest import Launcher, Backtest
from strategies.MA import strategy

# To test a specific stock, create the class with the symbol prop and pass the symbol.
# To test a specific strategy, create the class with the strategy prop and pass the strategy id.
# To test everything, create the class without any props.

Launcher(strategy=strategy, intraday=False, symbol='BTC-CAD', allow_fractional=True)
