import pandas as pd
import yfinance as yf
from datetime import date
import time


df = pd.read_csv('pages/data.csv')

today = date.today()

start_date = '1990-01-01'
end_date = today

#ticker = 'AAPL'
def change(ticker):

  data = yf.download(ticker, start_date, end_date)
  #time.sleep(4)
  #print(data)
  d2=data.iloc[-1,3]
  d1=data.iloc[-1,0]
  d12=d2-d1
  cha=(d12*100)/d2
  aa=str(cha)
  aa=aa[0:5]+"%"
  return aa,str(d12)

def nm(n):
    x=df.iloc[n, 1]
    return str(x)


num_rows = len(df.index)

xx="+-------------------Main Menu-------------------+"
x=""+xx
for i in range(0,num_rows,1):
   y=str(i+1)
   x1=y+". For "+nm(i)+" press "+y
   z=len(xx)-len(x1)-2
   t=" "*z
   x=x+"\n|"+x1+t+"|"
   if i==num_rows:
      x=x+"\n+-----------------------------------------------+"
   
print(x)