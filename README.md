# Stock Prediction AI 📈

A modern, machine learning-powered stock prediction application built with Python, Flask, and scikit-learn.

![Stock Prediction AI](https://images.unsplash.com/photo-1611974765270-ca1258634369?q=80&w=1000&auto=format&fit=crop)

## 🚀 Features

- **Real-time Predictions**: Uses Random Forest Classifier to predict Buy/Sell trends.
- **Live Data**: Fetches real-time market data using `yfinance`.
- **Technical Analysis**: Automatically calculates SMA (10/50), RSI, and Volume.
- **Modern UI**: Beautiful, responsive dark-mode interface with glassmorphism effects.
- **Precision Metrics**: Displays model confidence and precision scores.

## 🛠️ Tech Stack

- **Backend**: Python, Flask
- **ML/Data**: scikit-learn, pandas, numpy, yfinance
- **Frontend**: HTML5, CSS3, Vanilla JavaScript

## 🏃‍♂️ How to Run Locally

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd Stock_pred
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   python app.py
   ```

4. **Open in Browser**
   Navigate to `http://localhost:5000`

## 🌍 Deployment

### 🚀 Continuous Deployment with Render

This project includes a GitHub Actions workflow that automatically deploys to Render.

1.  **Create a Web Service on Render**:
    - Connect your GitHub repository.
    - Build Command: `pip install -r requirements.txt`
    - Start Command: `gunicorn app:app` (or `python app.py` if not using gunicorn)
2.  **Enable Auto-Deploy Hook**:
    - Go to your service settings in Render.
    - Scroll to **Deploy Hook** and copy the URL.
3.  **Configure GitHub Secret**:
    - In your GitHub repo, go to **Settings** > **Secrets and variables** > **Actions**.
    - Click **New repository secret**.
    - Name: `RENDER_DEPLOY_HOOK_URL`
    - Value: Paste your Render Deploy Hook URL.

Now, every push to the `main` branch will pass tests and then trigger a deployment on Render!

### Manual Local Run
1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd Stock_pred
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   python app.py
   ```

4. **Open in Browser**
   Navigate to `http://localhost:5001`

## ⚠️ Disclaimer

This application is for educational purposes only. Do not use it as financial advice.
