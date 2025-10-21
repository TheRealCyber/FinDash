import yfinance as yf

def fetch_stock_data(ticker="TCS.NS"):
    """
    Fetch current and recent stock data using yfinance.
    Default: TCS.NS (Tata Consultancy Services)
    """
    stock = yf.Ticker(ticker)

    # 1️⃣ Live market info
    info = stock.info
    current_price = info.get("currentPrice")
    previous_close = info.get("previousClose")
    change = None
    if current_price and previous_close:
        change = ((current_price - previous_close) / previous_close) * 100

    # 2️⃣ Recent historical prices (last 5 days)
    hist = stock.history(period="5d")

    print(f"\n📈 {ticker} — Latest Stock Information\n")
    print(f"Current Price: ₹{current_price}")
    print(f"Previous Close: ₹{previous_close}")
    if change is not None:
        print(f"Change: {change:.2f}%\n")

    print("Recent Closing Prices (Last 5 Days):")
    print(hist["Close"])

if __name__ == "__main__":
    # 👉 Example: Indian companies use the '.NS' suffix for NSE, '.BO' for BSE
    fetch_stock_data("^NSEI")   # Tata Consultancy Services
    # Try others:
    # fetch_stock_data("RELIANCE.NS")
    # fetch_stock_data("^NSEI")      # Nifty 50 Index
import yfinance as yf
import matplotlib.pyplot as plt

def plot_nsei_chart():
    # Fetch 5 days of NIFTY 50 data
    ticker = "^NSEI"
    stock = yf.Ticker(ticker)
    hist = stock.history(period="5d")

    # Extract date and close price
    dates = hist.index
    closes = hist["Close"]

    # Plot
    plt.figure(figsize=(7, 4))
    plt.plot(dates, closes, marker='o', linewidth=2)
    plt.title("📈 NIFTY 50 (Last 5 Days)", fontsize=14, pad=10)
    plt.xlabel("Date")
    plt.ylabel("Closing Price (₹)")
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    plot_nsei_chart()
