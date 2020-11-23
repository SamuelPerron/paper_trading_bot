import pandas as pd

class ApiPandas():
    def __init__(self, symbol):
        self.symbol = symbol
        self.df = self.get_df()
        self.df['RSI'] = self.get_rsi()
        self.df['MACD'] = self.get_macd()
        self.df['MACD Signal'] = self.get_macd_signal()
        self.df['5d_ma'] = self.get_ma(5)
        self.df['10d_ma'] = self.get_ma(10)
        self.df['50d_ma'] = self.get_ma(50)
        self.df['200d_ma'] = self.get_ma(200)


    def get_df(self):
        return pd.read_csv(f'data/{self.symbol}.csv', index_col=0)


    def get_rsi(self):
        period = 14
        close = self.df['Adj Close']
        delta = close.diff()
        delta = delta[1:] # Remove first entry

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

    def get_ema(self, period):
        return self.df['Adj Close'].ewm(span=period, adjust=False).mean()

    def get_macd(self):
        exp1 = self.df['Adj Close'].ewm(span=12, adjust=False).mean()
        exp2 = self.df['Adj Close'].ewm(span=26, adjust=False).mean()
        return exp1 - exp2

    def get_macd_signal(self):
        return self.df['MACD'].ewm(span=9, adjust=False).mean()
