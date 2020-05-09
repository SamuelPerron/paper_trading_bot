import csv

class PaperApi:
    def get(self, symbol, date):
        csv_file = csv.reader(open(f'data/{symbol}.csv', 'r'), delimiter=',')
        for i, row in enumerate(csv_file):
            if row[0] == date:
                return {
                    'symbol': symbol,
                    'open': row[1],
                    'close': row[4],
                    'volume': row[5],
                    '50d_avg': self.days_avg(i, 50, symbol),
                    '200d_avg': self.days_avg(i, 200, symbol),
                    'rsi': self.rsi(i, symbol)
                }

    def days_avg(self, i, nb_days, symbol):
        avg = 0
        minus_days = i - nb_days
        if minus_days > 0:
            avg_list = [
                float(r[4])
                for y, r in enumerate(csv.reader(open(f'data/{symbol}.csv', 'r'), delimiter=','))
                if y >= minus_days and y < i
            ]
            avg = sum(avg_list) / len(avg_list)
        return avg

    def closing_diff(self, i, nb_days, symbol):
        diffs = []
        minus_days = i - nb_days
        if minus_days > 0:
            diffs = [
                round(float(r[4]) * 100 / float(r[1]) - 100, 2)
                for y, r in enumerate(csv.reader(open(f'data/{symbol}.csv', 'r'), delimiter=','))
                if y >= minus_days and y < i
            ]
        return diffs

    def rsi(self, i, symbol):
        diffs = self.closing_diff(i, 14, symbol)
        if len(diffs) == 14:
            avg_pos_list = [n for n in diffs if n >= 0]
            avg_neg_list = [n for n in diffs if n < 0]
            len_avg_pos_list = len(avg_pos_list)
            len_avg_neg_list = len(avg_neg_list)

            if len_avg_pos_list == 0:
                calc = 100 - abs(100 / (1 + (abs(sum(avg_neg_list) / len_avg_neg_list) / 14)))
            elif len_avg_neg_list == 0:
                calc = 100 - abs(100 / (1 + (sum(avg_pos_list) / len_avg_pos_list) / 14) / 14)
            else:
                calc = 100 - abs(100 / (1 + ((sum(avg_pos_list) / len_avg_pos_list) / 14) / (abs(sum(avg_neg_list) / len_avg_neg_list) / 14)))
            return calc
