import os
from flask import Flask, render_template, request, jsonify
import yfinance as yf

app = Flask(__name__)

def analyze_stock(ticker):
    try:
        # Fetch recent historical data
        stock = yf.Ticker(ticker)
        hist = stock.history(period="6mo")
        if hist.empty:
            return {"error": "Invalid ticker or no data found"}
        
        # Simple Moving Average (SMA) calculations instead of LSTM/HMM
        hist['SMA_20'] = hist['Close'].rolling(window=20).mean()
        hist['SMA_50'] = hist['Close'].rolling(window=50).mean()
        
        last_close = hist['Close'].iloc[-1]
        sma20 = hist['SMA_20'].iloc[-1]
        sma50 = hist['SMA_50'].iloc[-1]
        
        # Basic rule-based logic for forecasting
        if sma20 > sma50 and last_close > sma20:
            action = "BUY 📈"
        elif sma20 < sma50 and last_close < sma20:
            action = "SELL 📉"
        else:
            action = "HOLD ⏸️"
            
        return {
            "ticker": ticker.upper(),
            "last_price": round(last_close, 2),
            "action": action,
            "sma_20": round(sma20, 2),
            "sma_50": round(sma50, 2)
        }
    except Exception as e:
        return {"error": str(e)}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/analyze')
def api_analyze():
    ticker = request.args.get('ticker', 'YKBNK.IS')
    return jsonify(analyze_stock(ticker))

if __name__ == '__main__':
    # Hugging Face Spaces defaults to port 7860
    app.run(host='0.0.0.0', port=7860)