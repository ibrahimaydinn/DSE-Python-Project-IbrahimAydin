import gradio as gr
import yfinance as yf

def analyze_stock(ticker):
    try:
        stock = yf.Ticker(ticker)
        hist = stock.history(period="6mo")
        if hist.empty:
            return "**Error:** Invalid ticker or no data found"
        
        hist['SMA_20'] = hist['Close'].rolling(window=20).mean()
        hist['SMA_50'] = hist['Close'].rolling(window=50).mean()
        
        last_close = hist['Close'].iloc[-1]
        sma20 = hist['SMA_20'].iloc[-1]
        sma50 = hist['SMA_50'].iloc[-1]
        
        if sma20 > sma50 and last_close > sma20:
            action = "BUY"
        elif sma20 < sma50 and last_close < sma20:
            action = "SELL"
        else:
            action = "HOLD"
            
        result = (
            f"### {ticker.upper()}\n"
            f"**Latest Price:** {last_close:.2f}\n\n"
            f"# {action}\n\n"
            f"**SMA 20:** {sma20:.2f} | **SMA 50:** {sma50:.2f}"
        )
        return result
    except Exception as e:
        return f"**Error:** {str(e)}"

# Build the Gradio UI
interface = gr.Interface(
    fn=analyze_stock,
    inputs=gr.Textbox(value="YKBNK.IS", label="Enter Ticker (e.g. THYAO.IS or AAPL)"),
    outputs=gr.Markdown(label="Analysis Result"),
    title="Stock Forecaster",
    description="Basic Technical Analysis Module using Simple Moving Averages."
)

if __name__ == "__main__":
    interface.launch()
