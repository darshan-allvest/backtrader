import backtrader as bt
import pandas as pd
from strategies.basic_strategy import GoldenCrossStrategy

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
# 2. Convert PX_LAST → Close only
# -----------------------------
# we only need closing price for this strategy; open/high/low are unused
# but we add a dummy volume column so the plotter doesn't complain
# and so the broker can fill market orders using "open" values (which will
# match the close since OHLC are identical).
# df['Open'] = df['PX_LAST']
# df['High'] = df['PX_LAST']
# df['Low'] = df['PX_LAST']
df['Close'] = df['PX_LAST']
# provide zeros for volume to satisfy the feed/plotter
df['Volume'] = 0

# -----------------------------
# 3. Create Cerebro Engine
# -----------------------------
cerebro = bt.Cerebro()
# fill orders at bar close instead of next bar open (our feed only has close)
cerebro.broker.set_coc(True)

# -----------------------------
# 4. Add Data Feed
# -----------------------------
data = bt.feeds.PandasData(
    dataname=df,
    datetime=None,   # because DATE is index
    # open='Open',
    # high='High',
    # low='Low',
    close='Close',
    volume='Volume',
    openinterest=None
)

cerebro.adddata(data)

# -----------------------------
# 5. Add Strategy
# -----------------------------
cerebro.addstrategy(GoldenCrossStrategy)

# -----------------------------
# 6. Broker Settings
# -----------------------------
cerebro.broker.setcash(100000)
# cerebro.broker.setcommission(commission=0.001)  # optional: 0.1%

start_val = cerebro.broker.getvalue()
print("Start Portfolio Value:", start_val)

# -----------------------------
# 7. Run Backtest
# -----------------------------
cerebro.run()

end_val = cerebro.broker.getvalue()
print("Final Portfolio Value:", end_val)
print("Total P/L:", end_val - start_val)

# -----------------------------
# 8. Plot Result (line chart since only close data)
# -----------------------------
cerebro.plot(style='line')