import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf
import ccxt
from ta.momentum import RSIIndicator
from ta.volatility import BollingerBands

# --- Setup ---
st.set_page_config(layout="wide")
st.title("💰 SMC Trading Bot")

# --- Sidebar Controls ---
with st.sidebar:
    st.header("⚙️ Settings")
    market = st.selectbox("Market", ["XAU/USD (Gold)", "BTC/USD", "EUR/USD (Forex)", "SPY (Stocks)"])
    timeframe = st.selectbox("Timeframe", ["1h", "4h", "1d"])

# --- Data Fetching Function ---
@st.cache_data
def get_data(market, timeframe):
    try:
        if market == "BTC/USD":
            exchange = ccxt.binance()
            data = exchange.fetch_ohlcv('BTC/USDT', timeframe, limit=1000)
            df = pd.DataFrame(data, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
            df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
        else:
            ticker_map = {
                "XAU/USD (Gold)": "GC=F",
                "EUR/USD (Forex)": "EURUSD=X",
                "SPY (Stocks)": "SPY"
            }
            
            yf_intervals = {"1d": "1d", "4h": "1h", "1h": "1h"}  # Mapping
            if timeframe not in yf_intervals:
                raise ValueError(f"Invalid timeframe '{timeframe}' for Yahoo Finance. Use '1d'.")
            
            df = yf.download(ticker_map[market], period="60d", interval=yf_intervals[timeframe])
            
            if df.empty:
                raise ValueError("Yahoo Finance returned empty data. Try a different timeframe.")
            
            df = df.reset_index()
            df = df.rename(columns={'Date': 'timestamp', 'Open': 'open', 'High': 'high', 'Low': 'low', 'Close': 'close'})
        
        required_cols = ['timestamp', 'open', 'high', 'low', 'close']
        if any(col not in df.columns for col in required_cols):
            raise ValueError("Missing essential columns!")
        
        return df[required_cols].copy()
    except Exception as e:
        st.error(f"Error fetching data: {str(e)}")
        return pd.DataFrame(columns=['timestamp', 'open', 'high', 'low', 'close'])

df = get_data(market, timeframe)

# --- SMC Trading Strategy ---
def smc_signals(df):
    if df.empty or 'timestamp' not in df.columns:
        return df
    
    signals = pd.DataFrame(index=df.index)
    signals['order_block'] = False
    signals['entry'] = False
    signals['exit'] = False
    signals['sl'] = np.nan
    
    for i in range(2, len(df)):
        try:
            prev2, prev1 = df.iloc[i-2], df.iloc[i-1]
            
            if (prev2['close'] > prev2['open']) and (prev1['close'] < prev1['open']):
                signals.at[i, 'order_block'] = True
                signals.at[i, 'entry'] = True
                signals.at[i, 'sl'] = prev1['low']
        except IndexError:
            continue
    
    return pd.concat([df, signals], axis=1)

df = smc_signals(df)

# --- Display Data ---
if not df.empty:
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    
    st.subheader(f"{market} Price Chart")
    st.line_chart(df.set_index('timestamp')['close'])
    
    signal_df = df[df['entry']]
    if not signal_df.empty:
        st.subheader("Trading Signals")
        st.dataframe(signal_df[['timestamp', 'close', 'sl']])
        
        st.subheader("Last Signal Details")
        last_signal = signal_df.iloc[-1]
        st.write(f"""
        - **Entry Time**: {last_signal['timestamp']}
        - **Entry Price**: {last_signal['close']:.2f}
        - **Stop Loss**: {last_signal['sl']:.2f}
        """)
    else:
        st.warning("No trading signals generated")
else:
    st.error("No valid data available - please try different parameters")

# --- Technical Indicators ---
if not df.empty:
    try:
        df['rsi'] = RSIIndicator(df['close']).rsi()
        bb = BollingerBands(df['close'])
        df['bb_width'] = bb.bollinger_wband()
        
        st.subheader("Technical Indicators")
        st.line_chart(df.set_index('timestamp')[['rsi', 'bb_width']])
    except Exception as e:
        st.warning(f"Couldn't calculate indicators: {str(e)}")

