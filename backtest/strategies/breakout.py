from .strategy import Strategy
import numpy as np

class Breakout(Strategy):
    def __init__(self):
        self.id = 2
        self.name = 'Breakout'
        self.position_size = 0.15
        self.stop_loss = 0.025

        self.lookback = 20
        self.ceiling, self.floor = 30, 10

    def check_for_entry_signal(self, data, df):
        index = df.index.get_loc(data.name)
        if index > 31:
            today_volatility = data['31d_std']
            yesterday_volatility = df.iloc[index - 1]['31d_std']
            delta_volatility = (today_volatility - yesterday_volatility) / today_volatility

            self.lookback = round(self.lookback * (1 + delta_volatility))
            if self.lookback > self.ceiling:
                self.lookback = self.ceiling
            elif self.lookback < self.floor:
                self.lookback = self.floor

            df['breakout'] = df['High'].rolling(window=self.lookback).max().shift().bfill()
            return data['Adj Close'] >= df.iloc[index]['breakout']
        else:
            return False

    def check_for_exit_signal(self, data, current_stop_loss):
        return data['Adj Close'] < current_stop_loss

strategy = Breakout()
