import math

class Strategy:
    def check_for_entry_signal(self, data):
        raise NotImplementedError()

    def check_for_exit_signal(self, data):
        raise NotImplementedError()

    def get_stop_loss(self, current_price, entry_price):
        initial_stop_loss = entry_price * (1 - self.stop_loss)
        if current_price <= entry_price:
            return initial_stop_loss

        initial_stop_loss_amount = entry_price - initial_stop_loss
        if current_price > entry_price + initial_stop_loss_amount:
            profit = current_price - entry_price
            trailing_multiplicator = math.floor(profit / initial_stop_loss_amount)
            current_trailing = initial_stop_loss * trailing_multiplicator
            return current_price + current_trailing
        elif current_price > entry_price:
            return initial_stop_loss
