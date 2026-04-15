import pandas as pd
import numpy as np
import yfinance as yf


df = pd.read_csv("nasdaq_1000_10y_clean.csv")

df["Date"] = pd.to_datetime(df["Date"])
df = df.sort_values(by=["Ticker", "Date"])


df["return"] = df.groupby("Ticker")["Close"].pct_change()


spy = yf.download(
    "SPY",
    start="2015-01-01",
    end="2025-01-01",
    auto_adjust=True,
    progress=False
)


spy = spy.reset_index()

spy.columns = [col[0] if isinstance(col, tuple) else col for col in spy.columns]

# Calculate SPY returns
spy["spy_return"] = spy["Close"].pct_change()

# Keep only needed columns
spy = spy[["Date", "spy_return"]]


df = df.merge(spy, on="Date", how="left")


results = []

for ticker, group in df.groupby("Ticker"):
    group = group.dropna()

    if len(group) < 2000:
        continue

    returns = group["return"]

    # Mean Return (annualized)
    mean_return = returns.mean() * 252

    # Volatility (annualized)
    volatility = returns.std() * np.sqrt(252)

    # Sharpe Ratio
    sharpe = mean_return / volatility if volatility != 0 else 0

    # Max Drawdown
    cumulative = (1 + returns).cumprod()
    peak = cumulative.cummax()
    drawdown = (cumulative - peak) / peak
    max_drawdown = drawdown.min()

    # 30-day return
    return_30d = group["Close"].pct_change(30).iloc[-1]

    # 90-day return
    return_90d = group["Close"].pct_change(90).iloc[-1]

    # Correlation with SPY
    correlation_spy = group[["return", "spy_return"]].corr().iloc[0, 1]

    results.append({
        "Ticker": ticker,
        "Mean Return": mean_return,
        "Volatility": volatility,
        "Sharpe Ratio": sharpe,
        "Max Drawdown": max_drawdown,
        "30 Day Return": return_30d,
        "90 Day Return": return_90d,
        "Correlation with SPY": correlation_spy
    })


features_df = pd.DataFrame(results)

# Clean bad values
features_df = features_df.replace([np.inf, -np.inf], np.nan)

features_df.to_csv("nasdaq_features_final.csv", index=False)

print(" Done. Features saved to nasdaq_features_final.csv")