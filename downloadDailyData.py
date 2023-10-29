import yfinance as yf
import pandas as pd
import os
from datetime import datetime, timedelta
from pytz import timezone

# Path to stock ticker list
ticker_file_path = "ASX\Australian.csv"

# Directory to save CSV files
output_dir = "ASX\AustralianStockData"


# Create output directory if it doesn't exist
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Read tickers from the specified file
tickers_df = pd.read_csv(ticker_file_path)
tickers = tickers_df['Ticker'].tolist()

# Define the time period (last 365 days)
start_date = (datetime.now() - timedelta(days=365)).strftime('%Y-%m-%d')
end_date = datetime.now().strftime('%Y-%m-%d')

# Define Eastern Standard Time
eastern = timezone('US/Eastern')

# List to hold tickers that triggered KeyError
key_error_tickers = []

# Download and save the data for each ticker
for ticker_symbol in tickers:
    try:
        # Download the data with 1-day interval
        stock_data = yf.download(ticker_symbol, start=start_date, end=end_date, interval="1d")

        # Check if the download was successful
        if isinstance(stock_data, pd.DataFrame) and isinstance(stock_data.index, pd.DatetimeIndex):
            # Localize the index to UTC and then convert to Eastern Standard Time
            stock_data.index = stock_data.index.tz_localize('UTC').tz_convert(eastern)
            
            # Select the required columns
            stock_data = stock_data[['Open', 'High', 'Low', 'Close', 'Volume']]
            
            # Save the data to a CSV file
            file_name = os.path.join(output_dir, f"{ticker_symbol.upper()}.csv")
            stock_data.to_csv(file_name)
            
            print(f"Downloaded data for {ticker_symbol} and saved to {file_name}")
        else:
            print(f"Failed to download data for {ticker_symbol}. It may be delisted or there may be an issue with the data.")

    except KeyError as e:
        print(f"KeyError encountered for {ticker_symbol}: {e}")
        key_error_tickers.append(ticker_symbol)

# Print the tickers that triggered a KeyError
if key_error_tickers:
    print("\nTickers that triggered KeyError:")
    print(", ".join(key_error_tickers))
else:
    print("\nAll tickers downloaded successfully without errors.")