# LangChain Stock Price Agent with Groq

An intelligent, real-time stock and share price retrieval agent built using the **LangChain** framework and powered by **Groq's fast LLM inference API** (defaulting to Llama-3 70B). The agent dynamically resolves company names to ticker symbols and retrieves current stock data using Yahoo Finance.

---

## Features
- **Dynamic Ticker Lookup**: Resolves semantic company names (e.g. "Apple" or "Microsoft") to correct Yahoo Finance ticker symbols (`AAPL`, `MSFT`) automatically.
- **Real-Time Data Retrieval**: Fetches current prices, daily ranges, open values, exchange details, and daily price movements.
- **Fast Inference**: Uses Groq's high-speed LLM inference models.
- **Interactive CLI & Direct Command Line**: Supports both single queries via command arguments and a stateful interactive conversation loop.

---

## File Architecture
- [tools.py](file:///C:/Users/palak/.gemini/antigravity/scratch/StockPriceAgent/tools.py) - Contains custom LangChain tools for searching tickers and fetching market prices.
- [agent.py](file:///C:/Users/palak/.gemini/antigravity/scratch/StockPriceAgent/agent.py) - Builds the LLM integration, defines the agent prompt, and compiles the agent executor.
- [main.py](file:///C:/Users/palak/.gemini/antigravity/scratch/StockPriceAgent/main.py) - CLI driver for single query arguments and interactive session loops.
- [requirements.txt](file:///C:/Users/palak/.gemini/antigravity/scratch/StockPriceAgent/requirements.txt) - List of required Python libraries.
- [.env.example](file:///C:/Users/palak/.gemini/antigravity/scratch/StockPriceAgent/.env.example) - Environment variables template.

---

## Getting Started

### 1. Prerequisites
- Python 3.9 or higher installed.
- A Groq API Key. Get one at [Groq Console](https://console.groq.com/keys).

### 2. Installation
Clone the repository (if not already cloned) and navigate to the directory:
```bash
git clone https://github.com/PalakSinha2505/StockPriceAgent.git
cd StockPriceAgent
```

Create a virtual environment:
```bash
python -m venv venv
```

Activate the virtual environment:
- **Windows (PowerShell)**:
  ```powershell
  .\venv\Scripts\Activate.ps1
  ```
- **macOS / Linux**:
  ```bash
  source venv/bin/activate
  ```

Install dependencies:
```bash
pip install -r requirements.txt
```

### 3. Configuration
Copy the `.env.example` file to `.env`:
```bash
cp .env.example .env
```
Open `.env` and fill in your Groq API Key:
```env
GROQ_API_KEY=gsk_...
```

---

## Usage

You can run the agent in two modes:

### A. Interactive Mode (Default)
Running `main.py` without arguments launches an interactive loop:
```bash
python main.py
```
**Example Session:**
```text
==================================================
   Stock Price Agent (powered by LangChain & Groq)
==================================================
Type your stock queries below. Type 'exit' or 'quit' to close.

You: What is NVIDIA's stock price?

Agent:
Company: NVIDIA Corporation (NVDA)
Exchange: NASDAQ
Current Price: 125.80 USD (Change: +2.45 / +1.99%)
Open: 123.35 USD
Day's Range: 123.10 - 126.15 USD
--------------------------------------------------
```

### B. Single Query Mode
Pass the prompt as a direct command line argument:
```bash
python main.py "Compare Google and Apple stock price"
```

### C. Advanced Configurations
Customize LLM parameters or models:
```bash
# Use a different model (e.g., Mixtral)
python main.py "How is Tesla trading?" --model mixtral-8x7b-32768

# Adjust temperature
python main.py --temp 0.2
```
