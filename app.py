"""
Created on Tue Jun 29 2023 4:00:00

@author: harkeganesh
"""
import matplotlib.pyplot as plt
import numpy as np
import streamlit as st

from models.black_scholes_model import black_scholes
from models.gbm_paths import geometric_brownian_paths

plt.style.use("bmh")
plt.rcParams["font.size"] = 12
plt.rcParams["figure.dpi"] = 300


def plot_simulated_paths(S0: float, St: np.ndarray, mu: float, sigma: float, N: int, 
                         T: int, paths: int,  highlight_max_min_paths: bool):
    time = np.linspace(0, T, N + 1)

    tt = np.full(shape=(paths, N + 1), fill_value=time).T

    fig, ax = plt.subplots(figsize=(12, 8))
    plt.plot(tt, St, color="black", linewidth=0.5)
    plt.xlim(tt[0][0], tt[-1][0])
    plt.xlabel("Time Increments")
    plt.ylabel("Stock Price")
    plt.title(
        "Realization of Geometric Brownian Motion \n $dS_t = \mu S_t dt + \sigma "\
        "S_t dW_t$\n $S_0 = {0}, \mu = {1}, \sigma = {2}$".format(S0, mu, sigma))
    if highlight_max_min_paths:
        max_path = St[:, St[-1].argmax()]
        min_path = St[:, St[-1].argmin()]
        plt.plot(tt[:, St[-1].argmax()], max_path, color="blue")
        plt.plot(tt[:, St[-1].argmin()], min_path, color="red")
    st.pyplot(fig)


def plot_price_distribution(prices: np.ndarray, strike_price: float, n_bins: int = 500):
    fig, ax = plt.subplots(figsize=(10, 6))

    n, bins, patches = plt.hist(prices, n_bins)

    for c, p in zip(bins, patches):
        if c > strike_price:
            plt.setp(p, "facecolor", "green")
        else:
            plt.setp(p, "facecolor", "blue")
    plt.axvline(strike_price, linestyle="--", color="red", label="strike")
    plt.title("Distribution of $S_{T}$")
    plt.xlabel("$S_{T}$")
    plt.ylabel("Count")
    plt.legend()
    st.pyplot(fig)


def main():
    st.title("Option Pricing with Geometric Brownian Motion")
    st.write("by [Ganesh Harke](https://www.linkedin.com/in/harkeganesh/)")

    st.sidebar.title("Option Pricing Parameters")

    # Get initial price stock
    S0 = st.sidebar.slider("Stock Price", min_value=100, max_value=500, value=100)

    # Mean returns of stock
    mu = st.sidebar.slider("Average Rate of Returns", min_value=0.01, max_value=0.2, 
                           value=0.05)

    # Volatility of stock
    sigma = st.sidebar.slider("Volatility", min_value=0.05, max_value=0.4, value=0.2)

    # Number of days for GBM
    N = st.sidebar.slider("Number of days to forecast", min_value=100, max_value=500, 
                          value=252)

    # Number of days to forecast
    T = N / 252

    # Length of time step
    dt = T / N

    # Number of simulations
    paths = st.sidebar.slider("Number of Paths", min_value=100, max_value=1000, 
                              value=500)

    highlight_max_min_paths = st.sidebar.checkbox("Show Max and Min paths", value=False)

    # st.sidebar.text("Option Pricing Details")

    strike_price = st.sidebar.slider("Option Strike Price (K)", min_value=S0-10, 
                                     max_value=S0+10, value=S0)

    simulated_paths = geometric_brownian_paths(S0, mu, sigma, N, dt, paths)

    plot_simulated_paths(S0, simulated_paths,  mu, sigma, N, T, paths, 
                         highlight_max_min_paths)

    payoffs = np.maximum(simulated_paths[-1, ]-strike_price, 0)
    option_price = np.mean(payoffs) * np.exp(-mu*T)

    bs_price = black_scholes(S0, strike_price, mu, sigma, T, "c")

    print(option_price, bs_price)

    
    plot_price_distribution(simulated_paths[-1, ], strike_price, )

    st.write("Option price  BS model:", round(bs_price, 4), \
             "Numberical Method:", round(option_price, 4))


if __name__ == "__main__":
    main()
