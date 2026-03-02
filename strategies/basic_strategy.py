import backtrader as bt

class BasicStrategy(bt.Strategy):
    def next(self):
        price = self.data.close[0]

        if not self.position and price < 100:
            print("BUY:", price)
            self.buy()

        elif self.position and price > 110:
            print("SELL:", price)
            self.sell()