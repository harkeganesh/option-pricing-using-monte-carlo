"""
Created on Tue Jun 29 2023 4:00:00

@author: harkeganesh
"""

from typing import Tuple

import numpy as np
from scipy.stats import norm


class BlackScholesModel:
    def __int__(self, stock_price: float, strike_price: float, risk_free_rate: float, time_to_expiry: float,
                volatility: float):
        self.S = stock_price
        self.K = strike_price
        self.r = risk_free_rate
        self.t = time_to_expiry
        self.sigma = volatility

    def d1(self):
        return (np.log(self.S / self.K) + (self.r + np.square(self.sigma) / 2) * self.t) / (self.sigma * np.sqrt(self.t))

    def d2(self, d1_):
        return d1_ - self.sigma * np.sqrt(self.t)

    def call_price(self):
        d1_ = self.d1()
        d2_ = self.d2(d1_)
        price = self.S * norm.cdf(d1_) - self.K * np.exp(-self.r * self.t) * norm.cdf(d2_)
        return np.round(price, 4)

    def put_price(self):
        d1_ = self.d1()
        d2_ = self.d2(d1_)
        price = self.K * np.exp(-self.r * self.t) * norm.cdf(-d2_) - self.S * norm.cdf(-d1_)
        return np.round(price, 4)


def black_scholes(S: float, K: float, r: float, sigma: float, t: float,
                  option_type: str = "c") -> Tuple[float, float]:
    """
    Calculates price of European option based on option type.

    S : float
      Underlying instrument price
    K : float
      Strike or exercise price of option
    r : float
      Risk free interest rate
    signma : float
      Volatility of underlying instrument
    t : int
      Time remaining for expiry of option
    option_type : str
      Type of option Call or Put
    """
    if option_type not in ("c", "p"):
        raise BaseException("Option type must be Call(c) or Put(p)")

    d1 = (np.log(S / K) + (r + np.square(sigma) / 2) * t) / (sigma * np.sqrt(t))

    d2 = d1 - sigma * np.sqrt(t)

    if option_type == "c":
        price = S * norm.cdf(d1) - K * np.exp(-r * t) * norm.cdf(d2)
    else:
        price = K * np.exp(-r * t) * norm.cdf(-d2) - S * norm.cdf(-d1)
    return np.round(price, 4)
