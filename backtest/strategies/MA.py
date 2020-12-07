from .strategy import Strategy

class MA(Strategy):
    def __init__(self):
        self.id = 1
        self.name = 'MA'
        self.position_size = 0.15
        self.stop_loss = 0.025
        self.rsi_floor = 30
        self.rsi_ceiling = 70

    def check_for_entry_signal(self, data, *args, **kwargs):
        return data['50d_ma'] > data['200d_ma']

    def check_for_exit_signal(self, data, current_stop_loss):
        return data['Adj Close'] < current_stop_loss

strategy = MA()
