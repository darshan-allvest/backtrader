import backtrader as bt


class BasicStrategy(bt.Strategy):
    params = (
        ("sma_period", 20),
    )

    def __init__(self):
        # Close price reference
        self.dataclose = self.datas[0].close

        # Track orders
        self.order = None

        # Indicator
        self.sma = bt.indicators.SimpleMovingAverage(
            self.datas[0], period=self.params.sma_period
        )

    def log(self, txt):
        dt = self.datas[0].datetime.date(0)
        print(f"{dt} | {txt}")

    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            return

        if order.status in [order.Completed]:
            if order.isbuy():
                self.log(f"BUY EXECUTED @ {order.executed.price:.2f}")
            else:
                self.log(f"SELL EXECUTED @ {order.executed.price:.2f}")

        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log("Order Failed")

        self.order = None

    def notify_trade(self, trade):
        if trade.isclosed:
            self.log(f"PROFIT, GROSS {trade.pnl:.2f}, NET {trade.pnlcomm:.2f}")

    def next(self):
        # Avoid early periods before SMA is ready
        if len(self) < self.params.sma_period:
            return

        # Skip if order pending
        if self.order:
            return

        # If no position → BUY condition
        if not self.position:
            if self.dataclose[0] > self.sma[0]:
                self.log(f"BUY SIGNAL @ {self.dataclose[0]:.2f}")
                self.order = self.buy(size=1)

        # If already in position → SELL condition
        else:
            if self.dataclose[0] < self.sma[0]:
                self.log(f"SELL SIGNAL @ {self.dataclose[0]:.2f}")
                self.order = self.sell(size=1)