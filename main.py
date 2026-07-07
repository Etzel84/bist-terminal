import streamlit as st
import yfinance as yf
import pandas as pd

# Hisse verisini çekerken ".IS" uzantısını daha güvenli yönetiyoruz
def get_hisse_data(ticker):
    try:
        # Kodun sonuna .IS ekliyoruz (BIST için zorunludur)
        symbol = f"{ticker.upper()}.IS"
        h = yf.Ticker(symbol)
        i = h.info
        
        # 'regularMarketPrice' bazen boş gelebilir, 'currentPrice' deniyoruz
        fiyat = i.get('currentPrice') or i.get('regularMarketPrice') or 0
        net_kar = i.get('netIncomeToCommon') or 0
        roe = i.get('returnOnEquity') or 0
        
        return {
            "Fiyat": fiyat,
            "Net Kar (M TL)": round(net_kar / 1000000, 1),
            "ROE": f"{round(roe * 100, 1)}%"
        }
    except Exception as e:
        return None

st.title("🛡️ BİST Master Karar Destek")

t = st.text_input("Hisse Kodu (örn: TUPRS):").upper()
if st.button("Analiz Et"):
    if not t:
        st.warning("Lütfen bir hisse kodu girin.")
    else:
        d = get_hisse_data(t)
        if d and d["Fiyat"] > 0:
            st.metric("Güncel Fiyat", f"{d['Fiyat']} TL")
            st.metric("Net Kar", f"{d['Net Kar (M TL)']} M TL")
            st.metric("ROE", d['ROE'])
        else:
            st.error(f"'{t}' hissesi bulunamadı. Kodun doğru olduğundan veya internet bağlantısından emin olun.")
