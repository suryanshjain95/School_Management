#
# STOCK ANALYSIS TOOL
# This script uses the yfinance library to fetch and display stock data.
# It can operate in online mode (fetching live data) or offline mode (using local CSV files).
# It also includes robust error handling for user input, file operations, and API calls.
#

import pandas as pd
import yfinance as yf
from datetime import date
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from tabulate import tabulate
import os

def printw(text):
    """Prints the given text in bright white."""
    BRIGHT_WHITE = '\033[97m'
    RESET = '\033[0m'
    print(f"{BRIGHT_WHITE}{text}{RESET}")

def printr(text):
    """Prints the given text in bright red."""
    BRIGHT_RED = '\033[91m'
    RESET = '\033[0m'
    print(f"{BRIGHT_RED}{text}{RESET}")

def printg(text):
    """Prints the given text in bright green."""
    BRIGHT_GREEN = '\033[92m'
    RESET = '\033[0m'
    print(f"{BRIGHT_GREEN}{text}{RESET}")

# Global variables
try:
    # Attempt to read the stocks from the CSV file.
    # This try-except block handles the case where the file doesn't exist.
    main_df = pd.read_csv('data.csv')
    printw("Stocks loaded from data.csv.")
except FileNotFoundError:
    printw("data.csv not found. Creating a new empty DataFrame.")
    # Define a new DataFrame if the file is not found
    main_df = pd.DataFrame(columns=['sno', 'Name', 'stock'])
    # Optional: Save an empty CSV to the disk so it's created
    main_df.to_csv("data.csv", index=False)
except Exception as e:
    printw(f"An error occurred while loading data.csv: {e}")
    # Define a new DataFrame if an error occurred while loading
    main_df = pd.DataFrame(columns=['sno', 'Name', 'stock'])


today = date.today()
start_date = '1990-01-01'
end_date = today

# =========================================================================
# === Data Manipulation Functions =========================================
# =========================================================================

def frame(df):
    """
    Prints a DataFrame in a formatted table.
    """
    if df.empty:
        printg("No data to display.")
        return
    
    # Check if the index is a DatetimeIndex and if so, convert it to a simple list for tabulate
    if isinstance(df.index, pd.DatetimeIndex):
        table = tabulate(df, headers=df.columns, tablefmt="grid")
    else:
        index_list = list(df.index)
        table = tabulate(df, headers=index_list, tablefmt="grid")
    
    return table

def add_stock(df):
    """
    Adds a new stock to the DataFrame and saves it to data.csv.
    """
    global main_df
    stock_name = input("Enter Stock name:").strip()
    stock_id = input("Enter Stock ID:").strip().upper()

    if not stock_name or not stock_id:
        printg("Stock name and ID cannot be empty.")
        return

    new_row = {'sno': len(main_df) + 1, 'Name': stock_name, 'stock': stock_id}
    main_df = pd.concat([main_df, pd.DataFrame([new_row])], ignore_index=True)
    main_df.to_csv("data.csv", index=False)
    printg(f"Stock '{stock_name}' with ID '{stock_id}' added successfully.")

def delete_stock(df):
    """
    Deletes a stock from the DataFrame and saves the changes.
    """
    global main_df
    stock_name_to_delete = input("Enter Stock name to delete:").strip()

    if stock_name_to_delete not in main_df['Name'].values:
        printg(f"Error: Stock '{stock_name_to_delete}' not found in the list.")
        return
        
    main_df = main_df.drop(main_df[main_df['Name'] == stock_name_to_delete].index)
    main_df.to_csv("data.csv", index=False)
    printg(f"Stock '{stock_name_to_delete}' deleted successfully.")

# =========================================================================
# === OFFLINE MODE FUNCTIONS (Local data) =================================
# =========================================================================

def historical_offline(ticker,data,file_path):
    """Fetches historical data from a local CSV file."""
    
    try:
        
        printr("\nHistorical Stock Prices (Offline Data)")
        printr(frame(data.tail())) # Display last 5 rows
    except FileNotFoundError:
        printr(f"Error: Data file for {ticker} not found at {file_path}.")
    except Exception as e:
        printr(f"An unexpected error occurred while reading the file: {e}")

def closeplot_offline(ticker):
    """Plots adjusted close price from a local CSV file."""
    
    try:
        
        img = mpimg.imread(f'//workspaces//School_Management//closeplot//{ticker}_closeplot.png')

        # Display the image
        plt.imshow(img)
        plt.axis('off') 
        plt.show()
    except Exception as e:
        printr(f"An error occurred while plotting: {e}")

def volume_offline(ticker):
    """Plots trading volume from a local CSV file."""
    
    try:
        img = mpimg.imread(f'//workspaces//School_Management//volume//{ticker}_volume.png')

        # Display the image
        plt.imshow(img)
        plt.axis('off') 
        plt.show()
        
    except Exception as e:
        printr(f"An error occurred while plotting: {e}")

# =========================================================================
# === ONLINE MODE FUNCTIONS (Live data via yfinance) ======================
# =========================================================================

def historical(ticker):
    """Fetches and displays historical data from yfinance."""
    try:
        data = yf.download(ticker, start_date, end_date)
        if data.empty:
            printg(f"No historical data found for ticker: {ticker}")
            return
        
        printg("\nHistorical Stock Prices")
        printg(frame(data.tail()))


    except Exception as e:
        printg(f"An unexpected error occurred while fetching data: {e}")

def closeplot(ticker):
    """Plots adjusted close price from yfinance data."""
    try:
        data = yf.download(ticker, start_date, end_date)
        if data.empty:
            printg(f"No data found to plot for ticker: {ticker}")
            return
        
        plt.figure(figsize=(10, 6))
        plt.plot(data['Close'])
        plt.xlabel('Date')
        plt.ylabel('Adjusted Close Price')
        plt.title(f'{ticker} Adjusted Close Price Data')
        plt.grid(True)
        plt.show()
        if os.path.exists(f'//workspaces//School_Management//volume//{ticker}_volume.png'): 
            os.remove(f'//workspaces//School_Management//volume//{ticker}_volume.png')
        
        plt.savefig(f'//workspaces//School_Management//closeplot//{ticker}_closeplot.png')
    except Exception as e:
        printg(f"An unexpected error occurred while plotting: {e}")

def volume(ticker):
    """Plots trading volume from yfinance data."""
    try:
        data = yf.download(ticker, start_date, end_date)
        if data.empty:
            printg(f"No data found to plot for ticker: {ticker}")
            return
            
        plt.figure(figsize=(10, 6))
        plt.plot(data['Volume'], color='orange')
        plt.xlabel('Date')
        plt.ylabel('Volume')
        plt.title(f'{ticker} Trading Volume')
        plt.grid(True)
        plt.show()
        if os.path.exists(f'//workspaces//School_Management//volume//{ticker}_volume.png'): 
            os.remove(f'//workspaces//School_Management//volume//{ticker}_volume.png')
        
        plt.savefig(f'//workspaces//School_Management//volume//{ticker}_volume.png')
    except Exception as e:
        printg(f"An unexpected error occurred while plotting: {e}")
          
def divident(ticker):
    """Displays dividend and stock split information."""
    try:
        stock = yf.Ticker(ticker)
        printg("\nDividends and Stock Splits")
        
        dividends = stock.dividends
        if not dividends.empty:
            printg("Dividends:")
            printg(dividends)
        else:
            print("No dividend data available for this stock.")

        splits = stock.splits
        if not splits.empty:
            printg("\nStock Splits:")
            printg(splits)
        else:
            printg("No stock split data available for this stock.")
    except Exception as e:
        printg(f"An error occurred while fetching data: {e}")

def statement(ticker):
    """Displays financial statements."""
    try:
        stock = yf.Ticker(ticker)
        printg("\nFinancial Statements (Annual)")

        printg("--- Income Statement ---")
        printg(frame(stock.financials))

        printg("\n--- Balance Sheet ---")
        printg(frame(stock.balance_sheet))
        
        printg("\n--- Cash Flow Statement ---")
        printg(frame(stock.cashflow))

    except Exception as e:
        printg(f"An error occurred while fetching data: {e}")

def quartely(ticker):
    """Displays quarterly financial statements."""
    try:
        stock = yf.Ticker(ticker)
        printg("\nQuarterly Financials")

        printg("--- Income Statement ---")
        printg(frame(stock.quarterly_financials))

        printg("\n--- Balance Sheet ---")
        printg(frame(stock.quarterly_balance_sheet))
        
        printg("\n--- Cash Flow Statement ---")
        printg(frame(stock.quarterly_cashflow))
    except Exception as e:
        printg(f"An error occurred while fetching data: {e}")

def share(ticker):
    """Displays institutional shareholders."""
    try:
        stock = yf.Ticker(ticker)      
        printg("\nInstitutional Shareholders")
        printg(frame(stock.institutional_holders))
    except Exception as e:
        printg(f"An error occurred while fetching data: {e}")

def infrom(ticker):
    """Displays company information."""
    try:
        stock = yf.Ticker(ticker)      
        printg("\nCompany Information")
        info = stock.info
        printg(f"Sector: {info.get('sector', 'N/A')}")
        printg(f"Industry: {info.get('industry', 'N/A')}")
        printg(f"Full Time Employees: {info.get('fullTimeEmployees', 'N/A')}")
        printg(f"Website: {info.get('website', 'N/A')}")
        printg("Summary:")
        printg(info.get('longBusinessSummary', 'N/A'))
    except Exception as e:
        printg(f"An error occurred while fetching data: {e}")

# =========================================================================
# === MENU NAVIGATION FUNCTIONS ===========================================
# =========================================================================

def search():
    """Searches for a stock name and opens the online sub-menu."""
    global main_df
    stock_name = input("Enter Stock name you want to search for:").strip()
    try:
        row = main_df[main_df['Name'] == stock_name]
        if row.empty:
            printg(f"Error: Stock '{stock_name}' not found in your list.")
            return
        
        ticker = row.iloc[0]['stock']
        data = yf.download(ticker, start_date, end_date)
        x="/workspaces/School_Management/data/"+str(ticker)+".csv"
        if not os.path.exists(x):
           data.to_csv(x)
        if os.path.exists(x):
           os.remove(x)
           data.to_csv(x)   
        sub_menu_online(ticker)
    except Exception as e:
        printg(f"An error occurred while searching: {e}")


def online_menu():
    """Main menu for online mode."""
    while True:   
        printg("\n+------------------Online Mode------------------+")
        printg("| 1. Press S to search stock                    |")
        printg("| 2. Press A to add a stock                     |")
        printg("| 3. Press D to delete a stock                  |")
        printg("| 4. Press Q to quit online mode                |")
        printg("+-----------------------------------------------+")
        user_input = input("Enter:").strip().lower()

        if user_input == "q":
            break
        elif user_input == "s":
            search()
        elif user_input == "a":
            add_stock(main_df)
        elif user_input == "d":
            delete_stock(main_df)  
        else:
            printg("Invalid option. Please try again.")


def offline_menu():
    """Main menu for offline mode."""
    global main_df
    num_rows = len(main_df.index)
    
    def nm(n):
      x=main_df.loc[n, "Name"]
      return str(x)

    while True:
        xx="+-----------------Offline mode------------------+"
        x=""+xx
        for i in range(0,num_rows,1):
           y=str(i+1)
           x1=y+". For "+nm(i)+" press "+y
           z=len(xx)-len(x1)-2
           t=" "*z
           x=x+"\n|"+x1+t+"|"
   
        printr(x+"\n|"+str(len(main_df)+1)+". Press A to add new stock                   "+"|\n|"+str(len(main_df)+2)+
           ". Press D to delete a stock                  "+
           "|\n| Q. Press Q to quit offline mode               |\n+-----------------------------------------------+")
        
        
        user_input = input("Enter:").strip().lower()

        if user_input == "q":
            break
        else:
            try:
                selection = int(user_input)
                if 1 <= selection <= len(main_df):
                    ticker = main_df.loc[selection - 1, "stock"]
                    sub_menu_offline(ticker)
                else:
                    printr("Invalid number. Please select a number from the list.")
            except ValueError:
                printr("Invalid input. Please enter a number or a valid command (A, D, Q).")


def sub_menu_offline(ticker):
    """Sub-menu for offline stock analysis."""

    file_path = f"data/{ticker}.csv"
    data1 = pd.read_csv(file_path,index_col="Price")
    data2=data1.drop(["Ticker","Date"], axis=0)

    while True: 
        printr(f"\n+-----------------Sub Menu Offline---------------------+")
        printr("| 1. For Historical Stock Prices press 1               |")    
        printr("| 2. For Adjusted Close Price press 2                  |")  
        printr("| 3. For Volume Data press 3                           |")
        printr("| B. For going back to main menu press B               |")
        printr("+------------------------------------------------------+")
        
        user_input = input("Enter:").strip().upper()
        if user_input == "B":
            break
        
        try:
            selection = int(user_input)
            if selection == 1:
                historical_offline(ticker,data2,file_path)
            elif selection == 2:
                closeplot_offline(ticker)
            elif selection == 3:
                volume_offline(ticker)
            else:
                printr("Invalid selection. Please choose 1, 2, 3, or B.")
        except ValueError:
            printr("Invalid input. Please enter a number or 'B'.")
     

def sub_menu_online(ticker):
    """Sub-menu for online stock analysis."""      
    while True:
        printg(f"\n+-----------------Sub Menu-----------------------------+")
        printg("| 1. For Historical Stock Prices press 1               |")    
        printg("| 2. For Adjusted Close Price press 2                  |")  
        printg("| 3. For Volume Data press 3                           |")
        printg("| 4. For Dividends and Stock Splits press 4            |") 
        printg("| 5. For Financial Statements press 5                  |") 
        printg("| 6. For Quarterly Financials press 6                  |")   
        printg("| 7. For Institutional Shareholders press 7            |")    
        printg("| 8. For Company Info press 8                          |")
        printg("| B. For going back to main menu press B               |")
        printg("+------------------------------------------------------+")  

        user_input = input("Enter:").strip().upper()
        if user_input == "B":
            break
        
        try:
            selection = int(user_input)
            if selection == 1:
                historical(ticker)
            elif selection == 2:
                closeplot(ticker)
            elif selection == 3:
                volume(ticker)
            elif selection == 4:
                divident(ticker)
            elif selection == 5:
                statement(ticker)
            elif selection == 6:
                quartely(ticker)
            elif selection == 7:
                share(ticker)
            elif selection == 8:
                infrom(ticker)
            else:
                printg("Invalid selection. Please choose a number from the menu.")
        except ValueError:
            printg("Invalid input. Please enter a number or 'B'.")

# =========================================================================
# === MAIN APPLICATION LOOP ===============================================
# =========================================================================

if __name__ == "__main__":
    while True:
        printw("\n+--------Choose App Mode--------+")
        print("\033[97m|\033[92m 1. Press N for Online Mode    \033[97m|")
        print("\033[97m|\033[91m 2. Press F for Offline Mode   \033[97m|")
        printw("| 3. Press Q to Quit            |")
        printw("+-------------------------------+")
        app_mode = input("Enter:").strip().lower()

        if app_mode == "n":
            online_menu()
        elif app_mode == "f":
            offline_menu()
        elif app_mode == "q":
            printw("Thank you for using the stock analysis tool. Goodbye!")
            break
        else:
            printw("Invalid mode. Please enter 'N', 'F', or 'Q'.")