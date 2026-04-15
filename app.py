import streamlit as st
import pandas as pd
import random

df_stocks = pd.read_csv('data and feature eng/clustered_stocks.csv')

# function to recommend stocks - (from modeling.ipynb)
def recommend_stocks(stock_name: str, n_recs: int = 10):
    stock_name = stock_name.lower()
    # work on a copy so we don't mutate original
    df = df_stocks.copy()  

    # ensure we have a lowercase ticker column to search
    if 'Ticker' in df.columns:
        df['__ticker_search'] = df['Ticker'].astype(str).str.lower()
    else:
        df['__ticker_search'] = df.index.astype(str).str.lower()

    # find the stock
    mask = df['__ticker_search'].str.contains(stock_name, na=False)
    if not mask.any():
        return pd.DataFrame(columns=['Ticker', 'Cluster'])

    stock_row = df[mask].iloc[0]
    cluster = stock_row['Cluster']  # expects Cluster already present in data_final

    # all stocks in same cluster
    cluster_stocks = df[df['Cluster'] == cluster]

    # pick up to 10 examples (adjust as desired)
    n = min(n_recs, len(cluster_stocks))
    if n == 0:
        return pd.DataFrame(columns=['Ticker', 'Cluster'])

    sampled_idx = random.sample(list(cluster_stocks.index), n)
    recommended_rows = cluster_stocks.loc[sampled_idx]
    return recommended_rows[['Ticker', 'Cluster']].reset_index(drop=True)

#================================================Streamlit UI Creation==================================================
# Streamlit App UI
st.title("Stock Recommendation System Using K-Means Clustering")
st.write("---------------------------------------------------------")
st.subheader("Market Supported:")
st.write("Nasdaq Composite")
st.write('---------------------------------------------------------')
# Searchable dropdown for stock name
# Get the list of stock names for the dropdown
stock_names = sorted(df_stocks['Ticker'].dropna().astype(str).unique())
stock_name = st.selectbox("Search for a stock you like:", options=stock_names)

# Button to trigger the recommendation
if st.button("Recommend Stocks"):
    recommendations_df = recommend_stocks(stock_name, n_recs=10)
    if recommendations_df.empty:
        st.info("No recommendations found for this stock.")
    else:
        st.write("### We recommend you these stocks:")
        st.dataframe(recommendations_df, use_container_width=True)