# Stock Recommendation System Using K-Means Clustering

This project implements an unsupervised machine learning, K-Means clustering-based recommendation engine for NASDAQ stocks. It groups stocks into clusters based on historical financial metrics like Mean Return, Volatility, Sharpe Ratio, Max Drawdown, and Correlation with the S&P 500, and uses a Streamlit app to recommend stocks from the same performance-based cluster.

## Project Structure

- `modeling.ipynb`: A Jupyter Notebook where data preprocessing, exploratory data analysis, PCA (Principal Component Analysis) dimensionality reduction, and clustering algorithm testing (K-Means, DBSCAN) are performed. The final clustering is evaluated and saved to disk.
- `app.py`: A Streamlit web application that serves as the interactive frontend. Users can select a NASDAQ stock, and the app returns a random sample of other recommended stocks from the same cluster.
- `data and feature eng/`: Folder containing raw, preprocessed, and final clustered datasets (e.g., `clustered_stocks.csv`, `nasdaq_features_final.csv`).

## Prerequisites

Ensure you have Python 3 installed. You will need the dependencies from your environment, mainly:
- `pandas`
- `numpy`
- `scikit-learn`
- `matplotlib`
- `seaborn`
- `streamlit`

You can install these via pip:
```bash
pip install pandas numpy scikit-learn matplotlib seaborn streamlit
```

## How to Run the App

1. **Activate your virtual environment** (if you are using one):
   - Windows: `.venv\Scripts\activate`
   - Mac/Linux: `source .venv/bin/activate`

2. **Run the Streamlit Application**:
   Navigate to the project root directory and run the following command in your terminal:
   ```bash
   streamlit run app.py
   ```

3. **Use the User Interface**:
   The command will open a local web server (usually at `http://localhost:8501`). Select your favorite stock from the searchable dropdown, click **"Recommend Stocks"**, and the app will display a list of stocks sharing a similar risk/return profile.

## Re-training / Data Updates

If you wish to update the stock features or alter the clustering hyperparameters:
1. Open and run through `modeling.ipynb`.
2. The final cell will recreate and save `data and feature eng/clustered_stocks.csv`.
3. Restart the Streamlit app to see your updated clusters.