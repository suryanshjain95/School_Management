import pandas as pd
import yfinance as yf
from datetime import date
#import time
import matplotlib.pyplot as plt


df = pd.read_csv('pages/data.csv')

today = date.today()

start_date = '1990-01-01'
end_date = today


# Get the data
     
def historical(ticker):
    data = yf.download(ticker, start_date, end_date)

    print("Historical Stock Prices")
    print(data.tail()) # Display last 5 rows

def closeplot(ticker):
    data = yf.download(ticker, start_date, end_date)

    # Plot adjusted close price data
    plt.plot(data['Close'])
    plt.xlabel('Date')
    print('Adjusted Close Price')
    plt.title(f'{ticker} Adjusted Close Price Data')
    plt.show()
    plt.savefig('my_plot.png')

def volume(ticker):
    data = yf.download(ticker, start_date, end_date)

    # Add more plots and data:
    print("Volume Data")
    plt.plot(data['Volume'], color='orange')
    plt.xlabel('Date')
    plt.ylabel('Volume')
    plt.title(f'{ticker} Trading Volume')
    plt.show()
    plt.savefig('my_plot.png')
          
def divident(ticker):
    # Dividends and Stock Splits
    print("Dividends and Stock Splits")
    stock = yf.Ticker(ticker)
    dividends = stock.dividends
    splits = stock.splits

    if not dividends.empty:
        print("Dividends:")
        print(dividends)
    else:
        print("No dividend data available for this stock.")

    if not splits.empty:
        print("Stock Splits:")
        print(splits)
    else:
        print("No stock split data available for this stock.")

def statement(ticker):
    # Financial Statements (Income Statement, Balance Sheet, Cash Flow)
    stock = yf.Ticker(ticker)
    print("Financial Statements")

    try:
        print("Income Statement (Annual)")
        print(stock.financials)
    except Exception as e:
        print(f"Could not retrieve annual income statement: {e}")

    try:
        print("Balance Sheet (Annual)")
        print(stock.balance_sheet)
    except Exception as e:
        print(f"Could not retrieve annual balance sheet: {e}")

    try:
        print("Cash Flow Statement (Annual)")
        print(stock.cashflow)
    except Exception as e:
        print(f"Could not retrieve annual cash flow statement: {e}")

def quartely(ticker):
    stock = yf.Ticker(ticker)
    # Quarterly Financials
    print("Quarterly Financials")
    try:
        print("Income Statement (Quarterly)")
        print(stock.quarterly_financials)
    except Exception as e:
        print(f"Could not retrieve quarterly income statement: {e}")

    try:
        print("Balance Sheet (Quarterly)")
        print(stock.quarterly_balance_sheet)
    except Exception as e:
        print(f"Could not retrieve quarterly balance sheet: {e}")

    try:
        print("Cash Flow Statement (Quarterly)")
        print(stock.quarterly_cashflow)
    except Exception as e:
        print(f"Could not retrieve quarterly cash flow statement: {e}")

def share(ticker):
    stock = yf.Ticker(ticker)      
    # Institutional Shareholders
    print("Institutional Shareholders")
    try:
        print(stock.institutional_holders)
    except Exception as e:
        print(f"Could not retrieve institutional holders: {e}")

def analyst(ticker):
    stock = yf.Ticker(ticker)      
    # Analyst Recommendations
    print("Analyst Recommendations")
    try:
        print(stock.recommendations)
    except Exception as e:
        print(f"Could not retrieve analyst recommendations: {e}")

def infrom(ticker):
    stock = yf.Ticker(ticker)      
    # Company Info (Summary)
    print("Company Information")
    try:
        info = stock.info
        print(f"Sector: {info.get('sector', 'N/A')}")
        print(f"Industry: {info.get('industry', 'N/A')}")
        print(f"Full Time Employees: {info.get('fullTimeEmployees', 'N/A')}")
        print(f"Website: {info.get('website', 'N/A')}")
        print("Summary:")
        print(info.get('longBusinessSummary', 'N/A'))
    except Exception as e:
        print(f"Could not retrieve company information: {e}")
            

#ticker = 'AAPL'
def change(ticker):
    data = yf.download(ticker, start_date, end_date)
    #time.sleep(4)
    #print(data)
    d2 = data.iloc[-1,3]
    d1 = data.iloc[-1,0]
    d12 = d2-d1
    cha = (d12*100)/d2
    aa = str(cha)
    aa = aa[0:5]+"%"
    return aa, str(d12)

def nm(n):
    x = df.iloc[n, 1]
    return str(x)


num_rows = len(df.index)
while True:
    xx = "+-------------------Main Menu-------------------+"
    x = ""+xx
    for i in range(0,num_rows,1):
        y = str(i+1)
        x1 = y+". For "+nm(i)+" press "+y
        z = len(xx)-len(x1)-2
        t = " "*z
        x = x+"\n|"+x1+t+"|"
   
      
    print(x+"\n+-----------------------------------------------+")

    inp = int(input("Enter:").lower())

    if inp == "q":
        quit()
    else:
        ticker = df.iloc[inp-1,2]
    while True:
        print("+-----------------Sub Menu-----------------+")
        print("|1.For Historical Stock Prices press 1     |")    
        print("|2.For Adjusted Close Price press 2        |")  
        print("|3.For Volume Data press 3                 |")
        print("|4.For Dividends and Stock Splits press 4  |") 
        print("|5.For Financial Statements press 5        |") 
        print("|5.For Quarterly Financials press 6        |")   
        print("|5.For Institutional Shareholders press 7  |")    
        print("|5.For Analyst Recommendations press 8     |")
        print("|5.For Company Info press 9                |")
        print("|10.For going back to main menu press B    |")
        print("+------------------------------------------+")

        innp = input("Enter:")
        if str(innp) == "B":
            quit()
        else:
            match innp:
                case 1:
                    historical(ticker)
                case 2:
                    closeplot(ticker)
                case 3:
                    volume(ticker)
                case 4:
                    divident(ticker)
                case 5:
                    statement(ticker)
                case 6:
                    quartely(ticker)
                case 7:
                    share(ticker)
                case 8:
                    analyst(ticker)
                case 9:
                    infrom(ticker)
                case _:
                    print("ERROR")
