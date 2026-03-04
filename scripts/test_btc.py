import backtrader as bt, pandas as pd

f='data/price.csv'
df=pd.read_csv(f,parse_dates=['DATE'])
df.set_index('DATE',inplace=True)
df=df.sort_index().dropna()
df['Close']=df['PX_LAST']
df['Volume']=0

class Tst(bt.Strategy):
    def __init__(self):
        self.dataclose=self.datas[0].close
        self.order=None
    def log(self,txt):
        print(f"{self.datas[0].datetime.date(0)} | {txt}")
    def next(self):
        if not self.position:
            self.log(f"signal buy at {self.dataclose[0]}")
            self.order=self.buy(size=1)
    def notify_order(self,order):
        if order.status in [order.Completed]:
            print('notify exec',order.executed.price,order.executed.size,order.executed.value,order.executed.comm)

cerebro=bt.Cerebro()
data=bt.feeds.PandasData(dataname=df,datetime=None,close='Close',volume='Volume')
cerebro.adddata(data)
cerebro.addstrategy(Tst)
cerebro.broker.setcash(10000)
cerebro.run()
