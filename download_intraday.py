from dotenv import ALPHA_VANTAGE_KEY, TEST
import requests
import re
import time
from math import ceil

RESULTS_PATH = './backtest/results/data/'

class ImportIntraday:
    def __init__(self, symbol, nb_slices, interval):
        self.symbol = symbol
        self.nb_slices = nb_slices if nb_slices <= 24 else 24
        self.interval = interval if interval in ['1min', '5min', '15min', '30min', '60min'] else '5min'
        self.base_url = f'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY_EXTENDED&apikey={ALPHA_VANTAGE_KEY}&symbol={self.symbol}&interval={self.interval}'
        self.start_import()


    def start_import(self):
        print(f'Importing {self.symbol}\'s {self.interval} intervals for last{" " + str(self.nb_slices) if self.nb_slices > 1 else ""} month{"s" if self.nb_slices > 1 else ""}')
        minutes = ceil(self.nb_slices / 5)
        print(f'This can take up to {minutes} minute{"s" if minutes > 1 else ""}')
        self.go_through_slices()


    def go_through_slices(self):
        current_year = 1
        current_month = 1
        for slice in range(self.nb_slices):
            current_year = current_year + 1 if slice == 12 else current_year
            current_month = 1 + slice if slice < 12 else (1 + slice) - 12 * (current_year - 1)
            query = f'year{current_year}month{current_month}'
            url = f'{self.base_url}&slice={query}'
            print(f'{self.symbol} | {query}')

            r = requests.get(url)
            try:
                void = r.json()
                print('Waiting 1 minute...')
                time.sleep(60)
                r = requests.get(url)
            except:
                received_csv = r.content.decode('utf-8')
                # remove -> time,open,high,low,close,volume
                received_csv = '\n'.join(received_csv.splitlines()[1:])
                file_path = f'{RESULTS_PATH}{self.symbol}-{self.interval}-{self.nb_slices}.csv'
                with open(file_path, 'a') as file:
                    file.write(received_csv)



i = ImportIntraday('PLUG', 17, '5min')
