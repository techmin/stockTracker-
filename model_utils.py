import yfinance as yf
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import precision_score

def fetch_stock_data(ticker: str, period="2y"):
    """Fetches stock data from Yahoo Finance."""
    stock = yf.Ticker(ticker)
    df = stock.history(period=period)
    if df.empty:
        raise ValueError(f"No data found for ticker {ticker}")
    return df

def calculate_technical_indicators(df: pd.DataFrame):
    """Adds technical indicators to the DataFrame."""
    df = df.copy()
    # Simple Moving Averages
    df["SMA_10"] = df["Close"].rolling(window=10).mean()
    df["SMA_50"] = df["Close"].rolling(window=50).mean()
    
    # RSI (Relative Strength Index)
    delta = df["Close"].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    rs = gain / loss
    df["RSI"] = 100 - (100 / (1 + rs))
    
    # Target: 1 if price goes up tomorrow, 0 otherwise
    df["Target"] = (df["Close"].shift(-1) > df["Close"]).astype(int)
    
    return df.dropna()

def train_model(df: pd.DataFrame):
    """Trains a Random Forest model."""
    predictors = ["Close", "Volume", "SMA_10", "SMA_50", "RSI"]
    
    # Split data
    train = df.iloc[:-100]
    test = df.iloc[-100:]
    
    model = RandomForestClassifier(n_estimators=100, min_samples_split=10, random_state=1)
    model.fit(train[predictors], train["Target"])
    
    # Evaluate
    preds = model.predict(test[predictors])
    precision = precision_score(test["Target"], preds)
    
    return model, precision, predictors

def predict_next_move(model, df: pd.DataFrame, predictors: list):
    """Predicts the next move based on the latest data."""
    last_row = df.iloc[[-1]][predictors]
    prediction = model.predict(last_row)[0]
    probability = model.predict_proba(last_row)[0][prediction]
    
    return "Buy" if prediction == 1 else "Sell", probability
