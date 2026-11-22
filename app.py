import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.graph_objects as go

st.set_page_config(page_title="Gold Market Monitor",page_icon="🥇",layout="wide")
st.title("🥇 Gold Market Monitor")
st.caption("Research dashboard • GC=F gold futures proxy, not broker XAUUSD spot • Not trading advice")
interval=st.selectbox("Timeframe",["1h","15m"],index=0)
period="60d" if interval=="1h" else "30d"

@st.cache_data(ttl=300,show_spinner=False)
def load(period,interval):
    data=yf.download("GC=F",period=period,interval=interval,auto_adjust=False,progress=False)
    if isinstance(data.columns,pd.MultiIndex):
        data.columns=data.columns.get_level_values(0)
    return data.dropna(subset=["Close"]).copy()

try:
    df=load(period,interval)
    if len(df)<55:
        st.warning("Not enough market data to calculate signals.")
        st.stop()
    df["EMA20"]=df["Close"].ewm(span=20,adjust=False).mean()
    df["EMA50"]=df["Close"].ewm(span=50,adjust=False).mean()
    df["PriorHigh"]=df["High"].shift(1).rolling(20).max()
    df["PriorLow"]=df["Low"].shift(1).rolling(20).min()
    # Exclude potentially incomplete current candle to avoid premature signals.
    completed=df.iloc[:-1].copy()
    last=completed.iloc[-1]
    bullish=last["EMA20"]>last["EMA50"]
    bearish=last["EMA20"]<last["EMA50"]
    breakout_up=last["Close"]>last["PriorHigh"]
    breakout_down=last["Close"]<last["PriorLow"]
    signal="WATCH BUY" if bullish and breakout_up else "WATCH SELL" if bearish and breakout_down else "WAIT"
    a,b,c=st.columns(3)
    a.metric("Last completed close (USD/oz)",f"{last['Close']:,.2f}")
    b.metric("Trend","Bullish" if bullish else "Bearish" if bearish else "Flat")
    c.metric("Rule-based signal",signal)
    st.caption(f"Last completed candle timestamp: {completed.index[-1]} (data-provider timezone). Source: Yahoo Finance via yfinance; may be delayed.")
    fig=go.Figure()
    view=completed.tail(150)
    fig.add_trace(go.Candlestick(x=view.index,open=view.Open,high=view.High,low=view.Low,close=view.Close,name="Gold futures"))
    fig.add_trace(go.Scatter(x=view.index,y=view.EMA20,name="EMA 20"))
    fig.add_trace(go.Scatter(x=view.index,y=view.EMA50,name="EMA 50"))
    fig.update_layout(height=480,xaxis_rangeslider_visible=False,margin=dict(l=5,r=5,t=25,b=5))
    st.plotly_chart(fig,use_container_width=True)
    with st.expander("Signal rules and limitations"):
        st.write("WATCH BUY: EMA20 above EMA50 and completed candle closes above previous 20-candle high. WATCH SELL: inverse. Otherwise WAIT. No AI learning, backtesting, broker connectivity, or order execution in this version. Free data availability and timestamps can vary.")
    if st.button("Refresh data"):
        load.clear()
        st.rerun()
except Exception as exc:
    st.error("Market data could not be loaded. Try refreshing later; free feeds may be unavailable.")
    st.caption(f"Technical detail: {type(exc).__name__}")
