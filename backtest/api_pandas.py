import pandas as pd
import os


class ApiPandas():
    def __init__(self, symbol):
        self.symbol = symbol
        self.df = self.get_df()
        self.df['RSI'] = self.get_rsi()
        self.df['5d_ma'] = self.get_ma(5)
        self.df['10d_ma'] = self.get_ma(10)
        self.df['50d_ma'] = self.get_ma(50)
        self.df['200d_ma'] = self.get_ma(200)

    def get_df(self):
        path = os.path.dirname(os.path.abspath(__file__))
        return pd.read_csv(f'{path}/data/{self.symbol}.csv', index_col=0)

    def get_rsi(self):
        period = 14
        close = self.df['Adj Close']
        delta = close.diff()
        delta = delta[1:]  # Remove first entry

        # Make the positive gains (up) and negative gains (down) Series
        up, down = delta.copy(), delta.copy()
        up[up < 0] = 0
        down[down > 0] = 0

        # Calculate the EWMA
        roll_up1 = up.ewm(span=period).mean()
        roll_down1 = down.abs().ewm(span=period).mean()

        # Calculate the RSI based on EWMA
        rs = roll_up1 / roll_down1
        return 100.0 - (100.0 / (1.0 + rs))

    def get_ma(self, period):
        return self.df['Adj Close'].rolling(window=period).mean()
