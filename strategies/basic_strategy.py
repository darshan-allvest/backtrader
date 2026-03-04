import backtrader as bt


class GoldenCrossStrategy(bt.Strategy):
    """A simple golden‑cross strategy that only relies on closing prices.

    The input data feed is expected to provide at least a `close` line. Open,
    high, low and volume fields aren't required and may be omitted.
    """

    params = (
        ("short_period", 50),
        ("long_period", 200),
    )

    def __init__(self):
        # Close price reference
        self.dataclose = self.datas[0].close

        # Track orders
        self.order = None

        # Golden Cross Indicators
        self.sma_short = bt.indicators.SimpleMovingAverage(
            self.datas[0], period=self.params.short_period
        )
        self.sma_long = bt.indicators.SimpleMovingAverage(
            self.datas[0], period=self.params.long_period
        )

        # Crossover detector
        self.crossover = bt.indicators.CrossOver(self.sma_short, self.sma_long)

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
            # report failure reason when available
            reason = ''
            if hasattr(order, 'reason') and order.reason:
                reason = f" reason={order.reason}"
            self.log(f"Order Failed{reason}")

        self.order = None

    def notify_trade(self, trade):
        if trade.isclosed:
            self.log(f"PROFIT, GROSS {trade.pnl:.2f}, NET {trade.pnlcomm:.2f}")

    def next(self):
        # Avoid early periods before both MAs are ready
        if len(self) < self.params.long_period:
            return

        # Skip if order pending
        if self.order:
            return

        # Golden Cross: 50-day MA crosses above 200-day MA → BUY
        if self.crossover[0] > 0 and not self.position:
            # Calculate how many shares we can afford with available cash
            available_cash = self.broker.get_cash()
            buy_price = self.dataclose[0]
            size = int(available_cash / buy_price)
            
            if size > 0:
                self.log(f"GOLDEN CROSS! BUY {size} @ {buy_price:.2f} (cash: {available_cash:.2f})")
                self.order = self.buy(size=size)
            else:
                self.log(f"GOLDEN CROSS SIGNAL but insufficient cash ({available_cash:.2f}) for price {buy_price:.2f}")

        # Death Cross: 50-day MA crosses below 200-day MA → SELL
        elif self.crossover[0] < 0 and self.position:
            self.log(f"DEATH CROSS! SELL @ {self.dataclose[0]:.2f}")
            self.order = self.sell(size=1)