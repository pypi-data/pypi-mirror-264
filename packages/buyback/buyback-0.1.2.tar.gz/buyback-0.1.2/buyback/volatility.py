import numpy as np
from scipy.stats import norm

def calculate_volatility(prices):
    """
    Calculate the daily volatility of a stock based on historical prices.
    
    Parameters:
    - prices: A list or numpy array of historical prices.
    
    Returns:
    - volatility: The daily volatility of the stock.
    - drift: The average daily return of the stock.
    """
    if not isinstance(prices, np.ndarray):
        prices = np.array(prices) # TODO: allow pandas series
    
    # Calculate daily returns
    returns = np.diff(prices) / prices[:-1]
    
    # Calculate the average daily return
    drift = returns.mean()
    
    # Calculate the daily volatility
    volatility = returns.std()# * np.sqrt(252) # 252 trading days in a year
    
    return volatility, drift

def calculate_var(P, sigma, Q=1, days=1, confidence_level=0.95):
    """
    Calculate VaR using the Variance-Covariance Method.
    
    Parameters:
    - P: The current value of the portfolio or asset.
    - sigma: The standard deviation of the portfolio's or asset's returns.
    - Q: The quantity of remaining shares to purchase. If 1, the VaR is calculated for the current portfolio value.
    - days: The number of days to calculate VaR for.
    - confidence_level: The confidence level (e.g., 0.95 for 95%).
    
    Returns:
    - VaR: The calculated Value at Risk at the specified confidence level.
    """
    if (days < 0):
        return 0
     
    Z = norm.ppf(confidence_level)
    VaR = P * Q * sigma * Z * np.sqrt(days)
    return VaR

def calculate_historical_var(returns, confidence_level=0.95): # Add more arguments to this function
    """
    Calculate VaR using the Historical Method.
    
    Parameters:
    - returns: A list or numpy array of historical returns.
    - confidence_level: The confidence level (e.g., 0.95 for 95%).
    
    Returns:
    - VaR: The calculated Value at Risk at the specified confidence level.
    """
    if not isinstance(returns, np.ndarray):
        returns = np.array(returns) # TODO: allow pandas series
    
    # Sort returns from worst to best
    sorted_returns = np.sort(returns)
    
    # Calculate the index for the VaR
    index = int((1 - confidence_level) * len(sorted_returns))
    
    # Return the VaR
    return abs(sorted_returns[index])

def calculate_historical_var_from_prices(prices, portfolio_value, confidence_level=0.95):
    """
    Calculate VaR using the Historical Method based on asset price data.
    
    Parameters:
    - prices: A list or numpy array of historical prices of the asset.
    - portfolio_value: The current total value of the portfolio or investment.
    - confidence_level: The confidence level (e.g., 0.95 for 95% confidence).
    
    Returns:
    - VaR: The calculated Value at Risk at the specified confidence level, representing
           the maximum expected loss in terms of the portfolio value.
    """
    if not isinstance(prices, np.ndarray):
        prices = np.array(prices) # TODO: allow pandas series
    
    # Calculate daily returns from price data
    returns = np.diff(prices) / prices[:-1]
    
    # Sort returns from worst to best
    sorted_returns = np.sort(returns)
    
    # Calculate the index for the VaR
    index = int((1 - confidence_level) * len(sorted_returns))
    
    # Calculate VaR based on the portfolio value and the return at the calculated index
    VaR = abs(sorted_returns[index]) * portfolio_value
    
    return VaR

def calculate_monte_carlo_var(P, mu, sigma, time_horizon, simulations, confidence_level=0.95):
    """
    Calculate VaR using the Monte Carlo Simulation Method.
    
    Parameters:
    - P: The current value of the portfolio or asset.
    - mu: The expected return of the portfolio or asset.
    - sigma: The standard deviation of the portfolio's or asset's returns.
    - time_horizon: The time horizon for the VaR calculation, in the same units as mu and sigma.
    - simulations: The number of simulations to run.
    - confidence_level: The confidence level (e.g., 0.95 for 95%).
    
    Returns:
    - VaR: The calculated Value at Risk at the specified confidence level.
    """
    # Generate random price paths
    random_shocks = np.random.normal(mu * time_horizon, sigma * np.sqrt(time_horizon), simulations)
    future_values = P + P * random_shocks # TODO: dedicated monte carlo function
    
    # Calculate VaR
    sorted_future_values = np.sort(future_values)
    index = int((1 - confidence_level) * len(sorted_future_values))
    VaR = abs(P - sorted_future_values[index])
    return VaR

def calculate_expected_shortfall(prices, confidence_level=0.95):  # AKA Conditional VaR (CVaR)
    """
    Calculate Expected Shortfall (ES) using the Historical Method.
    
    Parameters:
    - prices: A list or numpy array of historical prices.
    - confidence_level: The confidence level (e.g., 0.95 for 95%).
    
    Returns:
    - ES: The calculated Expected Shortfall at the specified confidence level.
    """
    if not isinstance(prices, np.ndarray):
        prices = np.array(prices) # TODO: allow pandas series
    
    # Calculate returns
    returns = np.diff(prices) / prices[:-1]
    
    # Sort returns from worst to best
    sorted_returns = np.sort(returns)
    
    # Calculate the index for the VaR
    index = int((1 - confidence_level) * len(sorted_returns))
    
    # Calculate the Expected Shortfall
    ES = abs(sorted_returns[:index].mean())
    return ES # TODO: multiply by portfolio value?