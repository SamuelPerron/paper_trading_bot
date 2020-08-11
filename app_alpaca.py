from dotenv import ALPACA_UID, ALPACA_SECRET
from alpaca import Alpaca
from datetime import datetime
import time

class TrainingBot:
    def __init__(self, profit_per, loss_per, position_size):
        self.api = Alpaca(
            ALPACA_UID, ALPACA_SECRET,
            '5Min',
        )
        self.period = 5 # Always in minutes for now (1, 5 or 15)
        self.minutes = self.get_minutes()
        self.symbols = []
        self.profit_per = profit_per
        self.loss_per = loss_per
        self.position_size = position_size
        self.hr = '--------------------------------------------------------------------------------'

        self.psa()
        self.run()


    def get_minutes(self):
        nb_in_hour = int(60 / self.period)
        return [self.period * i for i in range(1, nb_in_hour)]


    def run(self):
        open = False
        notified = False
        pre_market_fetched = False

        while True:
            if datetime.now().minute in self.minutes: # Every x minutes
                if self.api.are_markets_open(): # Not on the same line as to not spam the API
                    open = True
                    notified = False
                    pre_market_fetched = False

                    positions = self.api.positions()

                    for symbol in self.symbols:
                        data = self.api.compute(symbol)
                        self.check_buy(data, positions)

                    for position in positions:
                        data = self.api.compute(position.symbol)
                        self.check_sell(data, position)

                    self.psa()
                    time.sleep(60)

            if not open and not notified:
                print('Markets are closed.')
                notified = True

            # 5 minutes before markets open
            if not open and not pre_market_fetched and (datetime.now().minute == 55 and datetime.now().hour == 8):
                print(self.hr)
                self.symbols = self.api.fetch_pre_market()
                print('Trading symbols for the day:')
                for symbol in self.symbols:
                    print(f"{symbol['s']} | {symbol['p']} | {symbol['c']} | {symbol['v']}")
                pre_market_fetched = True


    def psa(self):
        account = self.api.get_account()
        print(self.hr)
        print(f"{datetime.now().strftime('%H:%M:%S')} | Portfolio value: {account['capital']}$ | Today P/L: {account['today_pl']}$ | Open positions: {account['nb_positions']}")
        print(self.hr)


    def check_buy(self, data, positions):
        if not self.api.in_positions(data['symbol']): # No duplicates
            if data['10_avg'] > data['50_avg'] and data['rsi'] <= 30: # Buy conditions
                max_price = self.position_size * self.api.capital()
                qty = int(round((max_price / data['close']), 0))
                if qty > 0:
                    self.api.buy(
                        data['symbol'],
                        qty,
                        take_profit=dict(
                            limit_price=data['close'] + (data['close'] * self.profit_per),
                        ),
                        stop_loss=dict(
                            stop_price=data['close'] - (data['close'] * self.loss_per),
                            limit_price=data['close'] - (data['close'] * self.loss_per),
                        )
                    )
                    return True
        print(f"{data['timestamp'].time()} |  --  | {data['symbol']: <4} | {data['close']}$ | {round(data['rsi'], 2)} rsi | {round(data['10_avg'], 2)}$ 10MA | {round(data['50_avg'], 2)}$ 50MA")


    def check_sell(self, data, position):
        if data['rsi'] is not None and data['rsi'] > 70:
            self.sell(data['symbol'], data['close'], position.qty)
            return True




TrainingBot(0.06, 0.03, 0.15)
