import streamlit as st
import pandas as pd
import yfinance as yf
from datetime import date
import time

st.set_page_config(layout="wide")

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
    n=n-1
    x=df.iloc[n, 1]
    return str(x)

def but(ticker):
  if ticker:
     st.session_state.ticker = ticker
     st.switch_page("pages/plot.py")
#with st.sidebar:
#    st.image("icon.jpg",width=100)
num_rows = len(df.index)

for i in range(0,num_rows,4):

    col1, col2, col3, col4 = st.columns(4, border=True)

    a1,a2=change(df.iloc[i,2])
    an="Details of "+df.iloc[i,1]
    with col1:
      if st.button(nm(i+1),key=df.iloc[i,2], type="tertiary"):
         but(df.iloc[i,2])
      st.metric(df.iloc[i,2],a1,a2[0:5])


    b1,b2=change(df.iloc[i+1,2])
    an="Details of "+df.iloc[i+1,1]
    with col2:
      if st.button(nm(i+2),key=df.iloc[i+1,2], type="tertiary"):
         but(df.iloc[i+1,2])
      st.metric(df.iloc[i+1,2],b1,b2[0:5])



    c1,c2=change(df.iloc[i+2,2])
    an="Details of "+df.iloc[i+2,1]
    with col3:
      if st.button(nm(i+3),key=df.iloc[i+2,2], type="tertiary"):
         but(df.iloc[i+2,2])
      st.metric(df.iloc[i+2,2],c1,c2[0:5])



    d1,d2=change(df.iloc[i+3,2])
    an="Details of "+df.iloc[i+3,1]
    with col4:
      if st.button(nm(i+4),key=df.iloc[i+3,2], type="tertiary"):
         but(df.iloc[i+3,2])
      st.metric(df.iloc[i+3,2],d1,d2[0:5])


