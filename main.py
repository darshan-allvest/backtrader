import backtrader as bt
import pandas as pd
from strategies.basic_strategy import BasicStrategy

# Load data
df = pd.read_csv("data/price.csv", parse_dates=["datetime"])
df.set_index("datetime", inplace=True)

# Create engine
cerebro = bt.Cerebro()

# Add data feed
data = bt.feeds.PandasData(dataname=df)
cerebro.adddata(data)

# Add strategy
cerebro.addstrategy(BasicStrategy)

# Capital
cerebro.broker.setcash(10000)

print("Start:", cerebro.broker.getvalue())

# Run
cerebro.run()

print("End:", cerebro.broker.getvalue())

# Plot
cerebro.plot()