import wbdata

import yfinance as yf
df = yf.download(["AAPL", "MSFT", "TSLA"], start="2015-01-01", end="2025-04-01")
df.to_csv("data/stock_prices.csv")


from datetime import datetime

data = wbdata.get_dataframe(
    indicators={"NY.GDP.MKTP.CD": "GDP", "FP.CPI.TOTL.ZG": "Inflation"},
    country=["FR", "DE", "IT"],
    data_date=(datetime(2015, 1, 1), datetime(2025, 4 1))
)
data.to_csv("data/worldbank_macro.csv")


from faker import Faker
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os

# Créer un dossier data s'il n'existe pas
os.makedirs('/mnt/data/data', exist_ok=True)

fake = Faker()
np.random.seed(42)

# -------------------------
# Données financières d'entreprises
# -------------------------
companies = [fake.company() for _ in range(10)]
years = list(range(2018, 2024))
financial_data = []

for company in companies:
    sector = fake.random_element(elements=("Tech", "Finance", "Healthcare", "Energy", "Retail"))
    for year in years:
        revenue = np.random.randint(100_000_000, 1_000_000_000)
        profit = int(revenue * np.random.uniform(0.05, 0.2))
        assets = revenue * np.random.uniform(1.2, 2.0)
        liabilities = assets * np.random.uniform(0.4, 0.8)
        employees = np.random.randint(200, 5000)
        region = fake.country()
        financial_data.append([company, sector, year, revenue, profit, assets, liabilities, employees, region])

df_financials = pd.DataFrame(financial_data, columns=[
    "Company", "Sector", "Year", "Revenue", "Profit", "Assets", "Liabilities", "Employees", "Region"
])

# -------------------------
# Données boursières simulées
# -------------------------
dates = pd.date_range(start="2023-01-01", end="2024-04-01", freq="B")
tickers = ["FAKE1", "FAKE2", "FAKE3", "FAKE4"]
stock_data = []

for ticker in tickers:
    price = np.random.uniform(50, 200)
    for date in dates:
        open_price = price + np.random.normal(0, 2)
        close_price = open_price + np.random.normal(0, 2)
        high = max(open_price, close_price) + np.random.uniform(0, 3)
        low = min(open_price, close_price) - np.random.uniform(0, 3)
        volume = np.random.randint(100000, 1000000)
        stock_data.append([date, ticker, round(open_price, 2), round(close_price, 2), round(high, 2), round(low, 2), volume])
        price = close_price  # update for next day

df_stocks = pd.DataFrame(stock_data, columns=[
    "Date", "Ticker", "Open", "Close", "High", "Low", "Volume"
])

# -------------------------
# Portefeuille utilisateur
# -------------------------
portfolio_data = []

users = ["alice", "bob", "carol"]
for user in users:
    for ticker in np.random.choice(tickers, 3, replace=False):
        shares = np.random.randint(10, 100)
        buy_price = np.random.uniform(60, 120)
        current_price = df_stocks[df_stocks["Ticker"] == ticker]["Close"].iloc[-1]
        sector = fake.random_element(elements=("Tech", "Finance", "Healthcare", "Energy"))
        portfolio_data.append([user, ticker, shares, round(buy_price, 2), round(current_price, 2), sector])

df_portfolio = pd.DataFrame(portfolio_data, columns=[
    "User", "Ticker", "Shares", "Buy_Price", "Current_Price", "Sector"
])

# Sauvegarde des fichiers
df_financials.to_csv("/mnt/data/data/financial_data.csv", index=False)
df_stocks.to_csv("/mnt/data/data/stock_data.csv", index=False)
df_portfolio.to_csv("/mnt/data/data/portfolio_data.csv", index=False)

import ace_tools as tools; tools.display_dataframe_to_user(name="Données simulées prêtes", dataframe=df_financials)


##python -m venv .venv
##source .venv/bin/activate  # ou .venv\Scripts\activate sous Windows