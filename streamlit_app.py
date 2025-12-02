# File name: app.py   (or streamlit_app.py)
import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="AIL-2045 Dual Engine", layout="wide")
st.title("AIL-2045 Bitcoin + cUSD Stablecoin Dual-Engine")
st.markdown("### Bitcoin for Growth • cUSD for Execution | 6 Real AfDB Projects | AIF 2025 Rabat")

# ========================= SIDEBAR =========================
st.sidebar.header("Bitcoin Growth Layer")
btc_seed = st.sidebar.slider("BTC Reserve Seed ($B)", 5.0, 150.0, 35.0, 5.0)
btc_cagr = st.sidebar.slider("BTC CAGR (%)", 5.0, 30.0, 15.0, 1.0) / 100
years = st.sidebar.slider("Forecast Horizon (Years)", 10, 30, 19)

st.sidebar.header("cUSD Stablecoin Layer")
stable_ratio = st.sidebar.slider("cUSD Issuance Ratio (%)", 50.0, 95.0, 80.0) / 100
stable_yield = st.sidebar.slider("Annual cUSD Lending Yield (%)", 5.0, 15.0, 8.0) / 100

st.sidebar.header("Other Capital")
bond_amount = st.sidebar.slider("Traditional Bonds ($B)", 0.0, 400.0, 200.0, 25.0)
fdi_amount = st.sidebar.slider("Crypto FDI ($B)", 0.0, 150.0, 50.0, 10.0)

# ========================= CALCULATIONS =========================
# Bitcoin growth
btc_2045 = btc_seed * (1 + btc_cagr) ** years
btc_gain = btc_2045 - btc_seed

# Stablecoin layer
initial_stable = btc_seed * stable_ratio
stable_2045 = initial_stable * (1 + stable_yield) ** years
stable_interest = stable_2045 - initial_stable

# Self-expanding loop (simplified but powerful)
avg_btc = btc_seed * ((1 + btc_cagr) ** years - 1) / (btc_cagr * years) if btc_cagr else btc_seed
extra_stable = (avg_btc - btc_seed) * stable_ratio * 0.7
extra_interest = extra_stable * stable_yield * (years / 2)

total_stable_capital = stable_2045 + extra_interest
total_dual = btc_2045 + total_stable_capital + bond_amount + fdi_amount * (1.20 ** 10)
gap_covered = total_dual / 1.5

# Jobs & savings
jobs = int(total_dual * 100_000)
savings = total_dual - (bond_amount * 1.4 + fdi_amount * 1.8 + btc_seed * 1.5)

# ========================= DASHBOARD =========================
c1, c2, c3 = st.columns(3)
c1.metric("BTC Value 2045", f"${btc_2045:,.1f}B", f"+${btc_gain:,.1f}B")
c2.metric("cUSD Capital 2045", f"${total_stable_capital:,.1f}B")
c3.metric("TOTAL Dual-Engine", f"${total_dual:,.1f}B", f"{gap_covered:.1%} of $1.5T gap")

c4, c5, c6 = st.columns(3)
c4.metric("Extra from Self-Expanding Loop", f"${extra_stable + extra_interest:,.1f}B")
c5.metric("Savings vs Traditional", f"${savings:,.1f}B")
c6.metric("Jobs Created", f"{jobs:,}")

# ========================= CHART (pure Streamlit – no matplotlib) =========================
years_list = list(range(2026, 2026 + years + 1))
btc_curve = [btc_seed * (1 + btc_cagr)**i for i in range(years + 1)]
stable_curve = [initial_stable * (1 + stable_yield)**i for i in range(years + 1)]
total_curve = [a + b for a, b in zip(btc_curve, stable_curve)]

df = pd.DataFrame({
    "Year": years_list,
    "Bitcoin Layer": btc_curve,
    "cUSD Stablecoin Layer": stable_curve,
    "Total Dual-Engine": total_curve
})

st.line_chart(df.set_index("Year")[["Bitcoin Layer", "cUSD Stablecoin Layer"]])
st.area_chart(df.set_index("Year")["Total Dual-Engine"], color="#FFD700")

st.markdown("**$1.5T Gap line**")
st.markdown("<hr style='border: 2px dashed red;'>", unsafe_allow_html=True)

# ========================= PROJECT PILOT =========================
st.subheader("Quick Project Pilot")
proj = st.selectbox("Choose real project", [
    "LAPSSET Corridor", "Rufiji Hydro Dam", "Eastern Angola Agri",
    "Egypt Pharma Biosimilars", "Nacala Corridor", "Nigeria Export Mfg Zones"
])
tranche = st.slider("Pilot tranche ($M)", 50, 1500, 500)

if "FDI" in proj or "Nigeria" in proj:
    pilot = tranche / 1000 * (1.22 ** 10)
else:
    pilot = tranche / 1000 * (1 + btc_cagr) ** years

st.success(f"**${tranche}M today → ${pilot:,.2f}B** in {years if 'FDI' not in proj else 10} years")

# ========================= DOWNLOAD =========================
csv = df.to_csv(index=False).encode()
st.download_button("Download Full Forecast", csv, "ail2045_dual_engine.csv", "text/csv")

st.caption("Africa United Corp • Bitcoin + cUSD • AIF 2025 Rabat • Booth A1")
