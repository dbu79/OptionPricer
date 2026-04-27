import streamlit as st
import numpy as np
import pandas as pd
from models import BlackScholes
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(
    page_title="Black-Scholes Calculator", 
    initial_sidebar_state="expanded",
    layout="wide")

st.title("Black-Scholes Option Price Calculator")

st.markdown("""
<style>
.metric-box {
    display: flex;
    flex-direction: column;
    align-items: center;
    text-align: center;
    background-color: #0b0f14;              
    border: 1px solid #1f2933;              
    border-radius: 6px;                     
    padding: 16px 18px;
            
}

.metric-label {
    font-size: 0.75rem;
    color: #8a99a8;                         
    text-transform: uppercase;
    letter-spacing: 1px;
    margin-bottom: 6px;
}

.metric-value {
    font-size: 1.8rem;
    font-weight: 600;
    color: #e6edf3;                         

}

.metric-call .metric-value {
    color: #00c853;  
                       
}

.metric-put .metric-value {
    color: #ff5252;                         
}

.metric-call {
    box-shadow: 0 0 10px rgba(0, 200, 83, 0.15);
}

.metric-put {
    box-shadow: 0 0 10px rgba(255, 82, 82, 0.15);
}
""", unsafe_allow_html=True)


# Sidebar
with st.sidebar:
    st.title("Black-Scholes Model Option Pricing")
    st.write("`Created by:`")
    linkedin = 'https://www.linkedin.com/in/daniel-butler-226b72331/'
    st.markdown(f'<a href="{linkedin}" target="_blank" style="text-decoration: none; color: inherit;"><img src="https://cdn-icons-png.flaticon.com/512/174/174857.png" width="25" height="25" style="vertical-align: middle; margin-right: 10px;">`Daniel Butler`</a>', unsafe_allow_html=True)
    st.divider()
    st.subheader("Black-Scholes Inputs:")
    # Black-Scholes Params
    S = st.number_input("Spot Price", min_value=0.00, value=100.00)
    K = st.number_input("Strike Price", 0.0, 1000.0, 100.00)
    T = st.number_input("Time to Maturity (Days)", 1, 365, value=240)
    r = st.number_input("Risk-Free Rate ", min_value=0.0, value=0.05)
    sigma = st.number_input("Volatility", min_value=0.01, value=0.30)
    
    st.divider()
    st.subheader("Heatmap Parameters")
    
    # Heatmap Parameters
    strike_range = st.slider(
        "Strike Price Range (% of Spot)",
        min_value=50,
        max_value=150,
        value=(80, 120),
        help="Range of strikes to display as percentage of current price")
    
    num_strikes = st.slider(
        "Number of Strike Prices",
        min_value=5,
        max_value=12,
        value=8,
        help="How many different strikes to calculate")
    
    max_days = st.slider(
        "Maximum Days to Expiry",
        min_value=30,
        max_value=365,
        value=180,
        help="Furthest expiration to show")
    
    num_expirations = st.slider(
        "Number of Expirations",
        min_value=5,
        max_value=12,
        value=8,
        help="How many different expiration dates")

input_data = {
    "Spot Price": [S],
    "Strike Price": [K], 
    "Time to Maturity": [T], 
    "Risk Free Rate": [r],
    "Volatility": [sigma]
}
input_df = pd.DataFrame(input_data)
st.table(input_df)

T_years = T / 365
values = BlackScholes(S, K, T_years, r, sigma)
call, put = values.call_put_prices()

col1, col2 = st.columns(2)

with col1:
    st.markdown(f"""
    <div class="metric-box metric-call">
        <div class="metric-label">Call Price</div>
        <div class="metric-value">${call:.3f}</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="metric-box metric-put">
        <div class="metric-label">Put Price</div>
        <div class="metric-value">${put:.3f}</div>
    </div>
    """, unsafe_allow_html=True)

def generate_heatmap_data(S, r, strike_range, sigma, num_strikes, max_days, num_expirations, option_type):
    min_strike = S * (strike_range[0] / 100)
    max_strike = S * (strike_range[1] / 100)
    strikes = np.linspace(min_strike, max_strike, num_strikes)

    days_to_expiry = np.linspace(1, max_days, num_expirations)

    price_matrix = np.zeros((num_strikes, num_expirations))

    for i, K in enumerate(strikes):
        for j, days in enumerate(days_to_expiry):
            T_years = days / 365
            bs = BlackScholes(S, K, T_years, r, sigma)
            call_price, put_price = bs.call_put_prices()

            price_matrix[i, j] = call_price if option_type == "Call" else put_price

    df = pd.DataFrame(
        price_matrix,
        index = np.round(strikes, 0),
        columns = np.round(days_to_expiry, 0).astype(int)
    )    

    return df

# Plot Heatmap
call_heatmap = generate_heatmap_data(
    S=S, r=r, sigma=sigma, 
    strike_range=strike_range,
    num_strikes=num_strikes, 
    max_days=max_days, 
    num_expirations=num_expirations,
    option_type="Call")

put_heatmap = generate_heatmap_data(
    S=S, r=r, sigma=sigma, 
    strike_range=strike_range,
    num_strikes=num_strikes, 
    max_days=max_days, 
    num_expirations=num_expirations,
    option_type="Put")

fig1, (ax_call, ax_put) = plt.subplots(1, 2, figsize=(20,8))

sns.heatmap(
    call_heatmap,
    ax=ax_call,
    annot=True,
    cmap='RdYlGn_r',  
    cbar_kws={'label': 'Option Price ($)'},
    fmt='.2f',
)
ax_call.invert_yaxis()

sns.heatmap(
    put_heatmap,
    ax=ax_put,
    annot=True,
    cmap="RdYlGn_r",
    cbar_kws={"label": "Option Price ($)"},
    fmt='.2f',
)
ax_put.invert_yaxis()

ax_call.set_title("Call Prices")
ax_call.set_xlabel("Days to Expiry")
ax_call.set_ylabel("Strike (% of Spot Price)")

ax_put.set_title("Put Prices")
ax_put.set_xlabel("Days to Expiry")
ax_put.set_ylabel("Strike (% of Spot Price)")

st.subheader("Option Price Heatmaps")
st.info("Change the heatmap parameters to visualize how strike price and time to expiration impact call and put option pricing -> The further out the money the cheaper the option")

st.pyplot(fig1)