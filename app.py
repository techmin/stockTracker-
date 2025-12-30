from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
from model_utils import fetch_stock_data, calculate_technical_indicators, train_model, predict_next_move
import os

app = Flask(__name__, static_folder='static')
CORS(app)

@app.route('/')
def index():
    return send_from_directory('static', 'index.html')

@app.route('/api/predict', methods=['POST'])
def predict():
    """Predict stock trend for a given ticker."""
    try:
        data = request.get_json()
        ticker = data.get('ticker', '').upper()
        
        if not ticker:
            return jsonify({'error': 'Ticker symbol is required'}), 400
        
        # Fetch and process data
        df = fetch_stock_data(ticker)
        df = calculate_technical_indicators(df)
        
        if len(df) < 100:
            return jsonify({'error': f'Not enough data to predict for {ticker}'}), 400
        
        # Train model and predict
        model, precision, predictors = train_model(df)
        prediction, probability = predict_next_move(model, df, predictors)
        
        # Get current price info
        current_price = float(df["Close"].iloc[-1])
        prev_price = float(df["Close"].iloc[-2])
        change = current_price - prev_price
        percent_change = (change / prev_price) * 100
        
        # Get technical indicators
        latest = df.iloc[-1]
        
        return jsonify({
            'ticker': ticker,
            'prediction': prediction,
            'confidence': float(probability),
            'precision': float(precision),
            'currentPrice': current_price,
            'priceChange': change,
            'percentChange': percent_change,
            'indicators': {
                'sma10': float(latest['SMA_10']),
                'sma50': float(latest['SMA_50']),
                'rsi': float(latest['RSI']),
                'volume': int(latest['Volume'])
            }
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/price/<ticker>', methods=['GET'])
def get_price(ticker):
    """Get current stock price."""
    try:
        ticker = ticker.upper()
        df = fetch_stock_data(ticker, period="5d")
        
        current_price = float(df["Close"].iloc[-1])
        prev_price = float(df["Close"].iloc[-2])
        change = current_price - prev_price
        percent_change = (change / prev_price) * 100
        
        return jsonify({
            'ticker': ticker,
            'price': current_price,
            'change': change,
            'percentChange': percent_change
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5001)
