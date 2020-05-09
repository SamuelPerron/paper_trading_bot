import csv

class PaperApi:
    def get(self, symbol, date):
        csv_file = csv.reader(open(f'data/{symbol}.csv', 'r'), delimiter=',')
        for i, row in enumerate(csv_file):
            if row[0] == date:
                fifty_d_avg = self.fifty_days_avg(i, symbol)
                minus_t_hundred_d = self.two_hundred_days_avg(i, symbol)
                return {
                    'symbol': symbol,
                    'open': row[1],
                    'close': row[4],
                    'volume': row[5],
                    '50d_avg': fifty_d_avg,
                    '200d_avg': minus_t_hundred_d,
                }

    def fifty_days_avg(self, i, symbol):
        fifty_d_avg = 0
        minus_fifty_d = i - 50
        if minus_fifty_d > 0:
            fifty_d_avg_list = [
                float(r[4])
                for y, r in enumerate(csv.reader(open(f'data/{symbol}.csv', 'r'), delimiter=','))
                if y >= minus_fifty_d and y < i
            ]
            fifty_d_avg = sum(fifty_d_avg_list) / len(fifty_d_avg_list)
        return fifty_d_avg

    def two_hundred_days_avg(self, i, symbol):
        t_hundred_d_avg = 0
        minus_t_hundred_d = i - 200
        if minus_t_hundred_d > 0:
            t_hundred_d_avg_list = [
                float(r[4])
                for y, r in enumerate(csv.reader(open(f'data/{symbol}.csv', 'r'), delimiter=','))
                if y >= minus_t_hundred_d and y < i
            ]
            t_hundred_d_avg = sum(t_hundred_d_avg_list) / len(t_hundred_d_avg_list)
        return t_hundred_d_avg
