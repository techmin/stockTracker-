from model_utils import fetch_stock_data, train_model, predict_next_move, calculate_technical_indicators

print("Fetching data...")
try:
    df = fetch_stock_data("NVDA")
    print(f"Data fetched: {len(df)} rows")
    
    print("Calculating indicators...")
    df = calculate_technical_indicators(df)
    
    print("Training model...")
    model, precision, predictors = train_model(df)
    print(f"Precision: {precision}")
    
    print("Predicting...")
    pred, prob = predict_next_move(model, df, predictors)
    print(f"Prediction: {pred} ({prob})")
    
except Exception as e:
    print(f"Error: {e}")
