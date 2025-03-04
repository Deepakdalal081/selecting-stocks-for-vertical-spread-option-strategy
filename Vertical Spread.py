import pandas as pd
import numpy as np
import yfinance as yf
import datetime as dt

# Define the date range for stock data analysis
end_date = dt.date.today()
start_date = end_date - dt.timedelta(days=45)

# List of stocks to analyze
stocks = ['ABB.NS', 'ADANIENSOL.NS', 'ADANIENT.NS', 'ADANIGREEN.NS', 'ADANIPORTS.NS', 'ADANIPOWER.NS',
          'ATGL.NS', 'AMBUJACEM.NS', 'APOLLOHOSP.NS', 'ASIANPAINT.NS', 'DMART.NS', 'AXISBANK.NS',
          'BAJAJ-AUTO.NS', 'BAJFINANCE.NS', 'BAJAJFINSV.NS', 'BAJAJHLDNG.NS', 'BANKBARODA.NS', 'BEL.NS',
          'BHEL.NS', 'BPCL.NS', 'BHARTIARTL.NS', 'BOSCHLTD.NS', 'BRITANNIA.NS', 'CANBK.NS', 'CHOLAFIN.NS',
          'CIPLA.NS', 'COALINDIA.NS', 'DLF.NS', 'DABUR.NS', 'DIVISLAB.NS', 'DRREDDY.NS', 'EICHERMOT.NS',
          'GAIL.NS', 'GODREJCP.NS', 'GRASIM.NS', 'HCLTECH.NS', 'HDFCBANK.NS', 'HDFCLIFE.NS', 'HAVELLS.NS',
          'HEROMOTOCO.NS', 'HINDALCO.NS', 'HAL.NS', 'HINDUNILVR.NS', 'ICICIBANK.NS', 'ICICIGI.NS',
          'ICICIPRULI.NS', 'ITC.NS', 'IOC.NS', 'IRCTC.NS', 'IRFC.NS', 'INDUSINDBK.NS', 'NAUKRI.NS', 'INFY.NS',
          'INDIGO.NS', 'JSWENERGY.NS', 'JSWSTEEL.NS', 'JINDALSTEL.NS', 'JIOFIN.NS', 'KOTAKBANK.NS', 'LTIM.NS',
          'LT.NS', 'LICI.NS', 'LODHA.NS', 'M&M.NS', 'MARUTI.NS', 'NHPC.NS', 'NTPC.NS', 'NESTLEIND.NS',
          'ONGC.NS', 'PIDILITIND.NS', 'PFC.NS', 'POWERGRID.NS', 'PNB.NS', 'RECLTD.NS', 'RELIANCE.NS',
          'SBILIFE.NS', 'MOTHERSON.NS', 'SHREECEM.NS', 'SIEMENS.NS', 'SBIN.NS', 'SUNPHARMA.NS', 'TVSMOTOR.NS',
          'TCS.NS', 'TATACONSUM.NS', 'TATAMOTORS.NS', 'TATAPOWER.NS', 'TATASTEEL.NS', 'TECHM.NS', 'TITAN.NS',
          'TORNTPHARM.NS', 'TRENT.NS', 'ULTRACEMCO.NS', 'UNIONBANK.NS', 'UNITDSPR.NS', 'VBL.NS', 'VEDL.NS',
          'WIPRO.NS', 'ZOMATO.NS', 'ZYDUSLIFE.NS']


# Function to calculate the Relative Strength Index (RSI)
def rsicalculate(data, period=14):
    delta = data["Close"].diff()  # Calculate price changes
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()  # Calculate average gains
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()  # Calculate average losses
    rs = gain / loss  # Relative Strength
    rsi = 100 - (100 / (1 + rs))  # RSI Calculation
    return rsi

# Lists to store stocks that meet spread criteria
bull_call_spread = []  # Stocks for Bull Call Spread
bear_call_spread = []  # Stocks for Bear Call Spread

# Iterate over each stock to analyze technical indicators
for stock in stocks:
    # Fetch historical stock data
    data = yf.download(stock, start=start_date, end=end_date, interval="1D", auto_adjust=True)
    
    # Calculate RSI
    data["RSI"] = rsicalculate(data)
    
    # Calculate Moving Average (21-day) and Standard Deviation
    data["MA_21"] = data["Close"].rolling(window=21).mean()
    data["Sd"] = data["Close"].rolling(window=21).std()
    
    # Calculate Bollinger Bands
    data["Upper_BB"] = data["MA_21"] + 2 * data["Sd"]  # Upper Band
    data["Lower_BB"] = data["MA_21"] - 2 * data["Sd"]  # Lower Band
    
    # Drop NaN values to avoid errors in indexing
    data = data.dropna()
    
    # Condition for Bear Call Spread (Stock near Upper Bollinger Band & RSI > 70)
    condition1 = (data["Upper_BB"].iloc[-1] < data["High"].iloc[-1]) & (data["RSI"].iloc[-1] > 70)
    
    # Condition for Bull Call Spread (Stock near Lower Bollinger Band & RSI < 30)
    condition2 = (data["Lower_BB"].iloc[-1] > data["Low"].iloc[-1]) & (data["RSI"].iloc[-1] < 30)
    
    # Assign stocks to respective strategy lists based on conditions
    if condition1.any():
        bear_call_spread.append(stock)
    elif condition2.any():
        bull_call_spread.append(stock)
    
# Display results
print("\n----------------------------")
print("Stocks suitable for Bear Call Spread:")
print(bear_call_spread)
print("----------------------------")
print("Stocks suitable for Bull Call Spread:")
print(bull_call_spread)
print("----------------------------")
print("Before placing any trades, thoroughly analyze the Greeks for informed decision-making.")
