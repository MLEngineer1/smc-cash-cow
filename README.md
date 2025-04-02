[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://blank-app-template.streamlit.app/)

# SMC Trading Bot

## 📌 Overview

SMC Trading Bot is a **Smart Money Concepts (SMC)** trading application built with **Streamlit**. It fetches market data, applies trading signals, and provides insights using technical indicators.

## 🚀 Features

- **Live Market Data**: Fetches OHLCV data from **Yahoo Finance** and **Binance (via CCXT)**.
- **SMC Trading Signals**: Identifies order blocks, entry points, and stop loss levels.
- **Technical Indicators**:
  - **Relative Strength Index (RSI)**
  - **Bollinger Band Width (BB Width)**
- **Interactive Charts**: Visualizes price movements and trading signals.
- **User-Friendly Interface**: Built with Streamlit for easy interaction.

## 🔧 Installation

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/yourusername/smc-trading-bot.git
cd smc-trading-bot
```

### 2️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 3️⃣ Run the App

```bash
streamlit run app.py
```

## 📊 Usage

1. Select a **Market** (e.g., BTC/USD, Gold, SPY, EUR/USD).
2. Choose a **Timeframe** (1h, 4h, 1d).
3. The app fetches data and applies SMC trading logic.
4. View:
   - **Price Charts** 📈
   - **Trading Signals** (Entry, Stop Loss)
   - **Technical Indicators** (RSI, Bollinger Bands)

## 🛠️ Technologies Used

- **Python**
- **Streamlit** (UI Framework)
- **Pandas** (Data Processing)
- **NumPy** (Numerical Computations)
- **Yahoo Finance (yfinance)** (Stock & Forex Data)
- **CCXT** (Crypto Exchange Data)
- **TA-Lib** (Technical Indicators)
- **Scikit-Learn** (Machine Learning - Logistic Regression for future expansion)

## 📌 To-Do

-

## 🤝 Contributing

1. Fork the repository.
2. Create a feature branch (`git checkout -b feature-name`).
3. Commit your changes (`git commit -m "Add new feature"`).
4. Push to the branch (`git push origin feature-name`).
5. Open a Pull Request.

## ⚡ License

This project is licensed under the **MIT License**.

---

🚀 **Happy Trading!**

