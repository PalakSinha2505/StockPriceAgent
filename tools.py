import requests
import yfinance as yf
from langchain.tools import tool

@tool
def get_stock_price(ticker: str) -> str:
    """
    Retrieves the current stock price and key market information for a given ticker symbol.
    Use this tool when you have a specific stock ticker (e.g. AAPL, MSFT, TSLA).
    """
    try:
        # yfinance expects tickers to be clean (e.g., uppercase)
        clean_ticker = ticker.strip().upper()
        stock = yf.Ticker(clean_ticker)
        info = stock.info
        
        # Check if we got any valid info
        if not info or ('regularMarketPrice' not in info and 'currentPrice' not in info and 'ask' not in info):
            # Attempt fallback to historical data
            hist = stock.history(period="1d")
            if not hist.empty:
                last_row = hist.iloc[-1]
                price = last_row['Close']
                currency = "USD"
                return (
                    f"Ticker: {clean_ticker}\n"
                    f"Current Price: {price:.2f} {currency} (retrieved from historical close)\n"
                    f"Open: {last_row['Open']:.2f}\n"
                    f"High: {last_row['High']:.2f}\n"
                    f"Low: {last_row['Low']:.2f}\n"
                    f"Volume: {int(last_row['Volume'])}"
                )
            return f"Error: No stock price or historical data found for ticker '{clean_ticker}'."
            
        name = info.get('longName') or info.get('shortName') or clean_ticker
        price = info.get('currentPrice') or info.get('regularMarketPrice') or info.get('ask')
        previous_close = info.get('regularMarketPreviousClose')
        currency = info.get('currency', 'USD')
        exchange = info.get('exchange', 'N/A')
        
        change_str = ""
        if price and previous_close:
            change = price - previous_close
            percent_change = (change / previous_close) * 100
            change_str = f" (Change: {change:+.2f} / {percent_change:+.2f}%)"

        result = [
            f"Company: {name} ({clean_ticker})",
            f"Exchange: {exchange}",
            f"Current Price: {price:.2f} {currency}{change_str}",
        ]
        
        open_p = info.get('dayOpen') or info.get('open')
        low_p = info.get('dayLow') or info.get('low')
        high_p = info.get('dayHigh') or info.get('high')
        
        if open_p: 
            result.append(f"Open: {open_p:.2f} {currency}")
        if low_p and high_p: 
            result.append(f"Day's Range: {low_p:.2f} - {high_p:.2f} {currency}")
            
        return "\n".join(result)
        
    except Exception as e:
        return f"Error retrieving stock price for ticker '{ticker}': {str(e)}"

@tool
def search_ticker(query: str) -> str:
    """
    Searches for stock ticker symbols matching a company name or search query.
    Use this tool when the user provides a company name (e.g. 'Apple', 'Microsoft') instead of a ticker.
    """
    url = f"https://query2.finance.yahoo.com/v1/finance/search?q={query}&quotesCount=5"
    try:
        response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
        if response.status_code == 200:
            data = response.json()
            quotes = data.get('quotes', [])
            if not quotes:
                return f"No stock ticker symbols found matching '{query}'."
            results = []
            for quote in quotes:
                symbol = quote.get('symbol')
                name = quote.get('shortname') or quote.get('longname') or "Unknown Name"
                exchange = quote.get('exchange')
                quote_type = quote.get('quoteType')
                results.append(f"- Ticker: {symbol} | Company Name: {name} | Exchange: {exchange} | Type: {quote_type}")
            return f"Found matching tickers for '{query}':\n" + "\n".join(results)
        else:
            return f"Error searching Yahoo Finance: HTTP status {response.status_code}."
    except Exception as e:
        return f"Exception searching for ticker matching '{query}': {str(e)}"
