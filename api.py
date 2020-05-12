import csv

class PaperApi:
    def get(self, symbol, date):
        csv_file = csv.reader(open(f'data/{symbol}.csv', 'r'), delimiter=',')
        for i, row in enumerate(csv_file):
            if row[0] == date:
                to_re = {
                    'symbol': symbol,
                    'open': row[1],
                    'close': row[4],
                    'volume': row[5],
                    '5d_avg': self.days_avg(i, 5, symbol),
                    '10d_avg': self.days_avg(i, 10, symbol),
                    '50d_avg': self.days_avg(i, 50, symbol),
                    '200d_avg': self.days_avg(i, 200, symbol),
                    'rsi': self.rsi(i, symbol, row[1], row[4]),
                }
                # if (i - 20) > 0:
                #     to_re['ema'] = self.ema(i, symbol, 0)
                return to_re

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

    def todays_value(self, i, symbol):
        for y, r in enumerate(csv.reader(open(f'data/{symbol}.csv', 'r'), delimiter=',')):
            if y == i:
                return float(r[4])


    def rsi(self, i, symbol, open, close):
        diffs = self.closing_diff(i, 14, symbol)
        if len(diffs) == 14:
            avg_pos_list = [n for n in diffs if n >= 0]
            avg_neg_list = [n for n in diffs if n < 0]
            len_avg_pos_list = len(avg_pos_list)
            len_avg_neg_list = len(avg_neg_list)

            # Step 1
            if len_avg_pos_list == 0:
                calc = 100 - abs(100 / (1 + (abs(sum(avg_neg_list) / len_avg_neg_list) / 14)))
            elif len_avg_neg_list == 0:
                calc = 100 - abs(100 / (1 + (sum(avg_pos_list) / len_avg_pos_list) / 14) / 14)
            else:
                calc = 100 - abs(
                    100 / (
                        1 + (
                            ((sum(avg_pos_list) / len_avg_pos_list) / 14) / (abs(sum(avg_neg_list) / len_avg_neg_list) / 14)
                        )
                    )
                )
            return calc

    def ema(self, i, symbol, rec):
        days = 20
        smoothing = 2
        todays_value = self.todays_value(i, symbol)
        todays_closing = self.days_avg(i, 20, symbol)
        smoothing_on_days_plus_one = (smoothing / (1 + days))
        if (i - days) >= 0 or rec == 0:
            yesterday_ema = self.ema(i - 1, symbol, 1)
            print(yesterday_ema, i, rec, (i - days))
            calc = (todays_value * smoothing_on_days_plus_one) + yesterday_ema * (1 - smoothing_on_days_plus_one)
            print(f't: {calc}')
            return calc
