from mcp.server.fastmcp import FastMCP
from model_utils import fetch_stock_data, calculate_technical_indicators, train_model, predict_next_move
import json

mcp = FastMCP("Stock Prediction")

@mcp.tool()
def predict_trend(ticker: str) -> str:
    """
    Predicts whether to Buy or Sell a stock based on technical indicators.
    Args:
        ticker: The stock ticker symbol (e.g., AAPL, MSFT).
    """
    try:
        df = fetch_stock_data(ticker)
        df = calculate_technical_indicators(df)
        
        if len(df) < 100:
            return f"Not enough data to predict for {ticker}"
            
        model, precision, predictors = train_model(df)
        prediction, prob = predict_next_move(model, df, predictors)
        
        return f"Prediction for {ticker}: {prediction} (Confidence: {prob:.2f})\nModel Precision on Test Data: {precision:.2f}"
    except Exception as e:
        return f"Error predicting for {ticker}: {str(e)}"

@mcp.tool()
def get_stock_price(ticker: str) -> str:
    """
    Gets the current stock price and daily change.
    Args:
        ticker: The stock ticker symbol.
    """
    try:
        df = fetch_stock_data(ticker, period="5d")
        current_price = df["Close"].iloc[-1]
        prev_price = df["Close"].iloc[-2]
        change = current_price - prev_price
        percent_change = (change / prev_price) * 100
        
        return f"{ticker} Price: ${current_price:.2f} ({change:+.2f} / {percent_change:+.2f}%)"
    except Exception as e:
        return f"Error fetching price for {ticker}: {str(e)}"

@mcp.resource("stock://{ticker}/info")
def get_stock_info(ticker: str) -> str:
    """
    Get fundamental information about a stock.
    """
    import yfinance as yf
    stock = yf.Ticker(ticker)
    info = stock.info
    # Filter for some key info to keep it concise
    keys = ['longName', 'sector', 'industry', 'marketCap', 'trailingPE', 'forwardPE', 'dividendYield']
    filtered_info = {k: info.get(k) for k in keys}
    return json.dumps(filtered_info, indent=2)

if __name__ == "__main__":
    mcp.run()
