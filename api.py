import csv

class PaperApi:
    def get(self, symbol, date):
        fifty_d_avg = 0
        t_hundred_d_avg = 0
        csv_file = csv.reader(open(f'data/{symbol}.csv', 'r'), delimiter=',')
        for i, row in enumerate(csv_file):
            if row[0] == date:
                minus_fifty_d = i - 50
                minus_t_hundred_d = i - 200
                if minus_fifty_d > 0:
                    fifty_d_avg_list = [
                        float(r[4])
                        for y, r in enumerate(csv.reader(open(f'data/{symbol}.csv', 'r'), delimiter=','))
                        if y >= minus_fifty_d and y < i
                    ]
                    fifty_d_avg = sum(fifty_d_avg_list) / len(fifty_d_avg_list)

                if minus_t_hundred_d > 0:
                    t_hundred_d_avg_list = [
                        float(r[4])
                        for y, r in enumerate(csv.reader(open(f'data/{symbol}.csv', 'r'), delimiter=','))
                        if y >= minus_t_hundred_d and y < i
                    ]
                    minus_t_hundred_d = sum(t_hundred_d_avg_list) / len(t_hundred_d_avg_list)

                return {
                    'symbol': symbol,
                    'open': row[1],
                    'close': row[4],
                    'volume': row[5],
                    '50d_avg': fifty_d_avg,
                    '200d_avg': minus_t_hundred_d,
                }
