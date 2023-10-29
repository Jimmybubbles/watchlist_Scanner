import yfinance as yf
import pandas as pd
import os
import talib
from datetime import datetime, timedelta

# Directory paths
input_directory = 'energy\energyData'
output_directory = 'energy\energyUpdate'

# Create output directory if it doesn't exist
if not os.path.exists(output_directory):
    os.makedirs(output_directory)

# Iterate over the files in the input directory
for file_name in os.listdir(input_directory):
    try:
        # Input file path for current file
        file_path = os.path.join(input_directory, file_name)
        ticker_symbol = os.path.splitext(file_name)[0]

        # Read the existing CSV file
        existing_data = pd.read_csv(file_path, index_col=0, parse_dates=True)

        # Find the last date in the existing data
        last_date = existing_data.index.max().strftime('%Y-%m-%d')

        # Define the time period for new data (from last date + 1 day)
        start_date = (datetime.strptime(last_date, '%Y-%m-%d') + timedelta(days=1)).strftime('%Y-%m-%d')
        end_date = datetime.now().strftime('%Y-%m-%d')

        # Download new data with 1-day interval
        new_data = yf.download(ticker_symbol, start=start_date, end=end_date, interval="1d")

        # Check if the DataFrame is empty
        if new_data.empty:
            print(f"No new data found for {ticker_symbol} in the specified date range.")
            continue

        # Localize the index to UTC
        new_data.index = new_data.index.tz_localize('UTC')

        # Calculate EMA 5
        new_data['EMA5'] = talib.EMA(new_data['Close'], timeperiod=5)

        # Calculate EMA 21
        new_data['EMA21'] = talib.EMA(new_data['Close'], timeperiod=21)

        # Calculate EMA 26
        new_data['EMA26'] = talib.EMA(new_data['Close'], timeperiod=26)

        # Calculate ATR 50
        new_data['ATR50'] = talib.ATR(new_data['High'], new_data['Low'], new_data['Close'], timeperiod=50)

        # Append the new data to the existing data
        combined_data = pd.concat([existing_data, new_data])

        # Save the combined data to a new CSV file
        output_file_path = os.path.join(output_directory, file_name)
        combined_data.to_csv(output_file_path)

        print(f"Updated data for {ticker_symbol} and saved to {output_file_path}")
    except Exception as e:
        print(f"Exception encountered for {ticker_symbol}: {str(e)}")
        print(f"Exception type: {type(e)}")

print("\nUpdate process completed.")