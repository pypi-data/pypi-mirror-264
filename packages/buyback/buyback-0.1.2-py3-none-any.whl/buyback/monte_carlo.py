import numpy as np
import pandas as pd
from scipy.stats import norm

def simulate_gbm(start_price, drift, volatility, days=252, num_simulations=1000):
    """
    Simulate price paths for an asset using Geometric Brownian Motion (GBM).
    
    Parameters:
    - start_price: The initial price of the asset.
    - drift: The annual drift rate of the asset's return. This can be considered
             as the expected return of the asset.
    - volatility: The annual volatility of the asset's return.
    - days: The number of trading days to simulate. The default is 252, the typical
            number of trading days in a year.
    - num_simulations: The number of price paths to simulate.
    
    Returns:
    - price_paths: A 2D numpy array where each column represents a simulated price path
                   of the asset, and each row represents the price of the asset at a different
                   time step.
    """
    dt = 1 / days  # Time increment, assuming 252 trading days in a year
    price_paths = np.zeros((days, num_simulations))
    price_paths[0] = start_price  # Initial price for all simulations

    # Generate paths
    for t in range(1, days):
        # Random shock from standard normal distribution
        random_shock = np.random.normal(0, 1, num_simulations)
        # Calculate price for next day using GBM formula
        price_paths[t] = price_paths[t - 1] * np.exp((drift - 0.5 * volatility**2) * dt + volatility * np.sqrt(dt) * random_shock)

    return price_paths


def calculate_return_statistics(df):
    """
    Calculate expected return (mu) and standard deviation (sigma) from simulated buyback data.
    
    Parameters:
    - df: Pandas DataFrame with columns ['shares_purchased', 'todays_VWAP', 'budget_remaining'].
    
    Returns:
    - mu: The expected daily return of the strategy.
    - sigma: The standard deviation of the daily returns.
    """
    raise NotImplementedError("Implement this function")
    # Calculate daily returns from VWAP and shares purchased
    df['daily_return'] = (df['shares_purchased'] * df['todays_VWAP']) / df['budget_remaining']
    
    # Calculate mu and sigma
    mu = df['daily_return'].mean()
    sigma = df['daily_return'].std()
    
    return mu, sigma