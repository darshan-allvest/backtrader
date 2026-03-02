import backtrader as bt
import pandas as pd
from strategies.basic_strategy import BasicStrategy

# -----------------------------
# 1. Load CSV
# -----------------------------
df = pd.read_csv("data/price.csv", parse_dates=["DATE"])

# Set DATE as index
df.set_index("DATE", inplace=True)

# Sort data by date (important)
df.sort_index(inplace=True)

# Remove any NaN rows
df.dropna(inplace=True)

# -----------------------------
# 2. Convert PX_LAST → OHLCV
# -----------------------------
df['Open'] = df['PX_LAST']
df['High'] = df['PX_LAST']
df['Low'] = df['PX_LAST']
df['Close'] = df['PX_LAST']
df['Volume'] = 0

# -----------------------------
# 3. Create Cerebro Engine
# -----------------------------
cerebro = bt.Cerebro()

# -----------------------------
# 4. Add Data Feed
# -----------------------------
data = bt.feeds.PandasData(
    dataname=df,
    datetime=None,   # because DATE is index
    open='Open',
    high='High',
    low='Low',
    close='Close',
    volume='Volume',
    openinterest=None
)

cerebro.adddata(data)

# -----------------------------
# 5. Add Strategy
# -----------------------------
cerebro.addstrategy(BasicStrategy)

# -----------------------------
# 6. Broker Settings
# -----------------------------
cerebro.broker.setcash(10000)
cerebro.broker.setcommission(commission=0.001)  # optional: 0.1%

print("Start Portfolio Value:", cerebro.broker.getvalue())

# -----------------------------
# 7. Run Backtest
# -----------------------------
cerebro.run()

print("Final Portfolio Value:", cerebro.broker.getvalue())

# -----------------------------
# 8. Plot Result
# -----------------------------
cerebro.plot(style='candlestick')