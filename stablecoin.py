import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="AIL-2045 Dual Engine", layout="wide")
st.title("AIL-2045 Bitcoin + Stablecoin Dual-Engine Model")
st.markdown("### Bitcoin for Growth • cUSD Stablecoin for Execution | 6 Real AfDB Projects | AIF 2025")

# ——————— SIDEBAR: GLOBAL PARAMETERS ———————
st.sidebar.header("Bitcoin Growth Layer")
btc_seed = st.sidebar.slider("BTC Reserve Seed ($B)", 5.0, 150.0, 35.0, 5.0)
btc_cagr = st.sidebar.slider("BTC CAGR (%)", 5.0, 30.0, 15.0, 1.0) / 100
years = st.sidebar.slider("Forecast Horizon (Years)", 10, 30, 19)

st.sidebar.header("Stablecoin Execution Layer")
stable_ratio = st.sidebar.slider("Stablecoin Issuance Ratio (%)", 50.0, 95.0, 80.0) / 100  # of BTC value
stable_yield = st.sidebar.slider("Annual Stablecoin Lending Yield (%)", 5.0, 15.0, 8.0) / 100

st.sidebar.header("Other Sources")
bond_amount = st.sidebar.slider("Traditional Bonds ($B)", 0.0, 400.0, 200.0, 25.0)
fdi_amount = st.sidebar.slider("Crypto FDI ($B)", 0.0, 150.0, 50.0, 10.0)

# ——————— CORE CALCULATIONS ———————
# 1. Bitcoin growth
btc_2045 = btc_seed * (1 + btc_cagr) ** years
btc_gain = btc_2045 - btc_seed

# 2. Stablecoin layer (cUSD issuance + compounding interest)
initial_stablecoins = btc_seed * stable_ratio                     # Year 0 issuance
stablecoins_2045 = initial_stablecoins * (1 + stable_yield) ** years
stable_interest_earned = stablecoins_2045 - initial_stablecoins

# 3. Self-expanding loop: every year we can mint more cUSD because BTC collateral grows
# Simplified: average collateral value over period → extra issuance capacity
avg_btc_value = btc_seed * ((1 + btc_cagr) ** years - 1) / (btc_cagr * years) if btc_cagr > 0 else btc_seed
extra_stable_issued = (avg_btc_value - btc_seed) * stable_ratio * 0.7   # 70% of new collateral value
extra_stable_interest = extra_stable_issued * stable_yield * (years / 2)  # avg half-period yield

total_stablecoin_capital = stablecoins_2045 + extra_stable_interest

# 4. Total dual-engine capital
total_dual_engine = btc_2045 + total_stablecoin_capital + bond_amount + fdi_amount * (1.20 ** 10)
gap_covered = total_dual_engine / 1.5

# 5. Traditional comparison & jobs
traditional = bond_amount * 1.4 + fdi_amount * 1.8 + btc_seed * 1.5  # conservative multiples
savings_vs_trad = total_dual_engine - traditional
jobs = int(total_dual_engine * 100_000)

# ——————— DASHBOARD ———————
col1, col2, col3 = st.columns(3)
col1.metric("BTC Value 2045", f"${btc_2045:,.1f}B", f"+${btc_gain:,.1f}B")
col2.metric("Stablecoin Capital 2045", f"${total_stablecoin_capital:,.1f}B", f"+${stable_interest_earned:,.1f}B interest")
col3.metric("Total Dual-Engine Capital", f"${total_dual_engine:,.1f}B", f"{gap_covered:.1%} of $1.5T gap")

col4, col5, col6 = st.columns(3)
col4.metric("Extra from Self-Expanding Loop", f"${extra_stable_issued + extra_stable_interest:,.1f}B")
col5.metric("Savings vs Traditional", f"${savings_vs_trad:,.1f}B")
col6.metric("Jobs Created", f"{jobs:,}")

# ——————— CHART ———————
year_list = list(range(2026, 2026 + years + 1))
btc_curve = [btc_seed * (1 + btc_cagr)**i for i in range(years + 1)]
stable_curve = [initial_stablecoins * (1 + stable_yield)**i for i in range(years + 1)]

fig, ax = plt.subplots(figsize=(12, 6))
ax.plot(year_list, btc_curve, label="Bitcoin Growth Layer", color="#F7931A", linewidth=4)
ax.plot(year_list, stable_curve, label="cUSD Stablecoin Layer", color="#00A86B", linewidth=4)
ax.fill_between(year_list, [a + b for a, b in zip(btc_curve, stable_curve)], color="gold", alpha=0.3, label="Total Dual-Engine")
ax.axhline(1500, color="red", linestyle="--", linewidth=3, label="$1.5T Financing Gap")
ax.set_title("AIL-2045 Dual-Engine: Bitcoin + cUSD Stablecoin", fontsize=16)
ax.set_ylabel("Capital ($ Billion)", fontsize=12)
ax.legend(fontsize=12)
ax.grid(True, alpha=0.3)
st.pyplot(fig)

# ——————— PROJECT PILOTS (unchanged, just for context) ———————
st.markdown("### 6 Real Project Pilots (use global parameters above)")
proj = st.selectbox("Select a real project", [
    "LAPSSET Corridor", "Rufiji Hydro Dam", "Eastern Angola Agri",
    "Egypt Pharma Biosimilars", "Nacala Corridor", "Nigeria Export Mfg Zones"
])

tranche = st.slider("Pilot tranche ($M)", 50, 1500, 500)
if "FDI" in proj or "Nigeria" in proj:
    pilot_2045 = tranche / 1000 * (1.22 ** 10)
else:
    pilot_2045 = tranche / 1000 * (1 + btc_cagr) ** years
st.success(f"**${tranche}M today → ${pilot_2045:,.2f}B** in {years if 'FDI' not in proj else 10} years")

# Export
df = pd.DataFrame({"Year": year_list, "Bitcoin": btc_curve, "Stablecoin": stable_curve})
csv = df.to_csv(index=False)
st.download_button("Download Full Forecast (CSV)", csv, "ail2045_dual_engine.csv")

st.caption("Africa United Corp | Bitcoin + cUSD = Unstoppable | AIF 2025 Rabat | Booth A1")
