import numpy as np
from scipy.stats import norm

class BlackScholes:
    def __init__(self, spot_price , strike_price, time_to_maturity, risk_free_rate, volatility):
        self.S = spot_price
        self.K = strike_price
        self.T = time_to_maturity
        self.r = risk_free_rate
        self.sigma = volatility
    
    def calc_d1_d2(self):
        vol_sqrt_t = self.sigma * np.sqrt(self.T)
        
        d1 = (np.log(self.S/self.K) + (self.r + self.sigma**2/2)*self.T)/vol_sqrt_t
        d2 = d1 - vol_sqrt_t

        return d1, d2 
    
    def call_put_prices(self):
        d1, d2 = self.calc_d1_d2()
        
        discount_factor = np.exp(-self.r * self.T)

        call_price = (self.S * norm.cdf(d1)) - (self.K * discount_factor * norm.cdf(d2))
        put_price = call_price + (self.K * discount_factor) - self.S
        
        return call_price, put_price

class Greeks(BlackScholes):
    def greeks(self, option_type):
        d1, d2 = self.calc_d1_d2()
        discount_factor = np.exp(-self.r * self.T)
        # 1. Delta, price sensitivity
        delta_call = norm.cdf(d1)
        delta_put = norm.cdf(d1) - 1 

        # 2. Gamma, delta's stability
        gamma = norm.pdf(d1)/(self.S * self.sigma * np.sqrt(self.T))

        # 3. Vega, volatility sensitivity
        vega = self.S * norm.pdf(d1) * np.sqrt(self.T)

        # 4. Theta, time sensitivity
        base_theta = -(self.S * norm.pdf(d1) * self.sigma) / (2 * np.sqrt(self.T))
        theta_call = base_theta - (self.r * self.K * discount_factor * norm.cdf(d2))
        theta_put = base_theta + (self.r * self.K * discount_factor * norm.cdf(-d2))

        # 5. Rho, sensitivity to interest rate
        rho_call = self.K * self.T * discount_factor * norm.cdf(d2)
        rho_put = -self.K * self.T * discount_factor * norm.cdf(-d2)

        if option_type == 'Call':
            return {
                "Delta": delta_call,
                "Gamma": gamma, 
                "Vega": vega, 
                "Theta": theta_call,
                "Rho": rho_call
                }
        elif option_type == "Put":
            return { 
                "Delta": delta_put,
                "Gamma": gamma, 
                "Vega": vega, 
                "Theta": theta_put,
                "Rho": rho_put
            }
        else:
            print("Please enter a valid option type [Put or Call].")

