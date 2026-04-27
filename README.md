# Black-Scholes Option Pricer 
Call/Put option pricing and heatmap using the Black-Scholes formula. 

https://blackscholes-optionpricing.streamlit.app/

## Project Overview
This project implements the Black-Scholes formula to price call and put options at given parameters, as well as a call and put heatmap to visualize different potential option prices. 

## Features

- **Black-Scholes Calculations**: Calculate theoretical call and put option prices
- **Interactive Heatmap Visualizations**: Side-by-side comparison of call and put option pricing surfaces
- **Customizable Parameters**: Adjust all Black-Scholes inputs and visualization settings
- **Moneyness Analysis**: View options across different strike prices (as % of spot price)
- **Time Decay Visualization**: See how option values change over time to expiration

## Heatmap

Each cell in the heatmap represents the price you would pay today for a specific option contract:

- **X-axis**: Days to expiration (time remaining on the contract)
- **Y-axis**: Strike price as percentage of spot price (moneyness)
- **Color intensity**: Option premium (red = expensive, green = cheap)
- **White dashed line**: At-the-money (ATM) strike where strike = spot price
