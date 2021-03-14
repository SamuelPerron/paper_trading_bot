from alpaca_paper.trader import Trader
from alpaca_paper.strategies.MACD import strategy

Trader(strategy)

# TODO: Multiple call to fetch premarket
# buys already hold symbol
# can't sell ??