import pandas as pd
import yfinance as yf
import random
import time
import requests


#getting nasdaq tickers
url = "https://raw.githubusercontent.com/datasets/nasdaq-listings/master/data/nasdaq-listed-symbols.csv"
df = pd.read_csv(url)

tickers = df['Symbol'].dropna().tolist()

#getting 1200 random stocks using random sample.
random.seed(42)
sampled_tickers = random.sample(tickers, min(1200, len(tickers)))  # oversample becasue we are going to filter some. 

#downloading data plus filtering
def chunk_list(lst, size):
    for i in range(0, len(lst), size):
        yield lst[i:i + size]

all_data = {}

for batch in chunk_list(sampled_tickers, 100):  # batch size = 100
    try:
        data = data = yf.download(
    batch,
    start="2015-01-01",
    end="2025-01-01",
    interval="1d",
    group_by="ticker",
    auto_adjust=True,
    threads=True,
    progress=False
)
        for ticker in batch:
            if ticker in data:
                all_data[ticker] = data[ticker]
        time.sleep(1)  # avoid rate limiting
    except Exception as e:
        print(f"Batch error: {e}")
        continue

#more filtring, here we filter illiquid stocks, and stocks that have missing values along with that we are also removing stocks that dont have atleast 10 years of data
clean_data = []
valid_tickers = []

for ticker, df in all_data.items():
    try:
        df = df.dropna()

        # Require ~10 years of data (~2000+ trading days)
        if len(df) < 2000:
            continue

        # Remove illiquid stocks
        if df['Volume'].mean() < 100000:
            continue

        # Ensure no missing values remain
        if df.isnull().sum().sum() > 0:
            continue

        df['Ticker'] = ticker
        clean_data.append(df)
        valid_tickers.append(ticker)

        # Stop once we hit 1000 good stocks
        if len(valid_tickers) >= 1000:
            break

    except Exception as e:
        continue

#combining data
if len(clean_data) == 0:
    raise ValueError("No valid data collected. Try increasing sample size.")

final_df = pd.concat(clean_data)
final_df.reset_index(inplace=True)

# Sort for consistency
final_df = final_df.sort_values(by=["Ticker", "Date"])

#saving the file 
final_df.to_csv("nasdaq_1000_10y_clean.csv", index=False)

print(f"Saved {len(valid_tickers)} tickers to CSV.")