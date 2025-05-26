import yfinance as yf
import matplotlib.pyplot as plt
from datetime import date
#import pandas as pd # Import pandas

dic={"Apple":"AAPL", "Tesla":"TSLA", "Microsoft":"MSFT","Mullen":"MULN","Bit Brother":"BETSF","Paragon":"PRGNF","Smart for Life":"SMFL","Wearable Devices":"WLDS","Kohl's Corporation":"KSS","Affymax":"AFFY","Wolfspeed":"WOLF","Beyond Meat":"BYND","American Rebel":"AREB","Entegris":"ENTG","CAVA Group":"CAVA","Amcor":"AMCR","Tapestry":"TPR","CarMax":"KMX","Pool Corporation":"POOL","Exelixis":"EXEL"}

today = date.today()

# Set the start and end date
start_date = '1990-01-01'
end_date = today # Set default to today

def main(ticker):
     # Get the data
     data = yf.download(ticker_symbol, start_date, end_date)

     if not data.empty:
          st.subheader("Historical Stock Prices")
          print(data.tail()) # Display last 5 rows

          # Plot adjusted close price data
          plt.plot(data['Close'])
          plt.xlabel('Date')
          plt.label('Adjusted Close Price')
          plt.title(f'{ticker_symbol} Adjusted Close Price Data')
          plt.show()

          # Add more plots and data:
          print("Volume Data")
          plt.plot(data['Volume'], color='orange')
          plt.xlabel('Date')
          plt.ylabel('Volume')
          plt.title(f'{ticker_symbol} Trading Volume')
          plt.show()

          # Dividends and Stock Splits
          print("Dividends and Stock Splits")
          stock = yf.Ticker(ticker_symbol)
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

          # Financial Statements (Income Statement, Balance Sheet, Cash Flow)
          print("Financial Statements")

          try:
              print("### Income Statement (Annual)")
              print(stock.financials)
          except Exception as e:
              print(f"Could not retrieve annual income statement: {e}")

          try:
              print("### Balance Sheet (Annual)")
              print(stock.balance_sheet)
          except Exception as e:
              print(f"Could not retrieve annual balance sheet: {e}")

          try:
              print("### Cash Flow Statement (Annual)")
              print(stock.cashflow)
          except Exception as e:
              print(f"Could not retrieve annual cash flow statement: {e}")

          # Quarterly Financials
          print("Quarterly Financials")
          try:
              print("### Income Statement (Quarterly)")
              print(stock.quarterly_financials)
          except Exception as e:
              print(f"Could not retrieve quarterly income statement: {e}")

          try:
              print("### Balance Sheet (Quarterly)")
              print(stock.quarterly_balance_sheet)
          except Exception as e:
              print(f"Could not retrieve quarterly balance sheet: {e}")

          try:
              print("### Cash Flow Statement (Quarterly)")
              print(stock.quarterly_cashflow)
          except Exception as e:
              print(f"Could not retrieve quarterly cash flow statement: {e}")
      
          # Institutional Shareholders
          print("Institutional Shareholders")
          try:
              print(stock.institutional_holders)
          except Exception as e:
              print(f"Could not retrieve institutional holders: {e}")
      
          # Analyst Recommendations
          print("Analyst Recommendations")
          try:
              print(stock.recommendations)
          except Exception as e:
              print(f"Could not retrieve analyst recommendations: {e}")
      
          # Company Info (Summary)
          print("Company Information")
          try:
              info = stock.info
              print(f"**Sector:** {info.get('sector', 'N/A')}")
              print(f"**Industry:** {info.get('industry', 'N/A')}")
              print(f"**Full Time Employees:** {info.get('fullTimeEmployees', 'N/A')}")
              print(f"**Website:** {info.get('website', 'N/A')}")
              print("**Summary:**")
              print(info.get('longBusinessSummary', 'N/A'))
          except Exception as e:
              print(f"Could not retrieve company information: {e}")
            
     else:
          print(f"Could not retrieve data for {ticker_symbol}. Please check the ticker symbol or date range.")
            
