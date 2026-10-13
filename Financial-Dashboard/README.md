# Financial Comparative Analysis Dashboard

An interactive financial dashboard built with Python and Streamlit to compare two stocks using historical market data, financial metrics, visualizations, and AI-powered analysis.

> **Note:** The AI analysis feature has not been tested with an active OpenAI API account. A valid API key and access to the configured model are required to use this feature. API usage may incur additional costs.

Developed as a learning project to practice Python application development, data visualization, financial data analysis, and OpenAI API integration.

## Features

- Compare two stocks using customizable ticker symbols and date ranges.
- Visualize historical prices using line, bar, and candlestick charts.
- Calculate 20-day moving averages and daily returns.
- Display key price statistics and company information.
- Compare closing prices and historical volatility.
- Download stock data as CSV files.
- Generate an AI-powered comparative report using the OpenAI API.

## Technologies

- Python
- Streamlit
- OpenAI API
- yfinance
- Pandas and NumPy
- Plotly

## Installation

Clone the repository and navigate to the project directory.

Create a virtual environment:

```bash
python -m venv .venv
```

Activate it on Windows:

```powershell
.venv\Scripts\activate
```

On macOS or Linux:

```bash
source .venv/bin/activate
```

Install the required dependencies:

```bash
pip install -r requirements.txt
```

## Configuration

The AI analysis feature requires an OpenAI API key with access to the model configured in the application.

Set the `OPENAI_API_KEY` environment variable before running the application.

**Windows PowerShell:**

```powershell
$env:OPENAI_API_KEY="your-api-key"
```

**macOS / Linux:**

```bash
export OPENAI_API_KEY="your-api-key"
```

Without a configured API key, the application stops during initialization. API usage may incur additional costs.

## Run the Application

```bash
streamlit run financialDashboard.py
```

## Disclaimer

This project is intended for educational purposes only and does not provide professional financial advice. Market data availability and AI-generated results may vary and should be independently verified.