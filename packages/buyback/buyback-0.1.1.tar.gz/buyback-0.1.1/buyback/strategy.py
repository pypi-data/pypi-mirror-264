import pandas as pd

from .constants import *

# class Strategy:
#     def __init__(self, strategy):
#         raise NotImplementedError("You should implement this!")

#     def execute(self, data):
#         raise NotImplementedError("You should implement this!")


def buy_shares(desired_shares, price, remaining_budget=-1, remaining_shares=-1):
    """
    Calculate the number of shares to purchase.
    
    Parameters:
    - desired_shares: The number of shares to purchase.
    - price: The price of the shares.
    - remaining_budget: The remaining budget to purchase shares. If -1, the budget is not considered.
    - remaining_shares: The remaining shares to purchase. If -1, the remaining shares is not considered.
    
    Returns:
    - shares: The number of shares to purchase.
    - cost: The cost of purchasing the shares.
    - remaining_budget: The remaining budget after purchasing shares.
    - remaining_shares: The remaining shares after purchasing shares.
    """
    # Calculate the number of shares to purchase
    shares = desired_shares
    if remaining_budget > -1:
        shares = min(shares, remaining_budget / price)
    if remaining_shares > -1:
        shares = min(shares, remaining_shares)
    shares = int(shares)

    # Calculate the cost of purchasing the shares
    cost = shares * price

    # Calculate the remaining budget and shares
    if remaining_budget > -1:
        remaining_budget -= cost
    if remaining_shares > -1:
        remaining_shares -= shares

    return shares, cost, remaining_budget, remaining_shares


def fixed_participation_rate(volumes, participation_rate, target_shares=-1): # TODO: add budget and target shares
    """
    Calculate the number of shares to purchase based on the participation rate.
    
    Parameters:
    - volumes: A pandas Series of traded volumes.
    - participation_rate: The percentage of the volume to participate in.
    - target_shares: The number of shares to purchase. If -1,
    
    Returns:
    - shares: The number of shares to purchase.
    """
    # Make sure the volumes are a pandas Series
    if not isinstance(volumes, pd.Series):
        volumes = pd.Series(volumes)

    # If the participation rate is a percentage, convert it to a fraction
    if participation_rate > 1:
        participation_rate = participation_rate / 100

    # Calculate the number of shares to purchase
    shares = volumes * participation_rate

    # Round to the nearest whole number
    shares = shares.round().astype(int)
    
    return shares

def calculate_progress(df, budget=-1, target_shares=-1, cols=[SHARES_COL, PRICE_COL], adjust=True):
    """
    Calculate the progress of the strategy over time. Calculates cost, cumulative cost, cumulative shares, remaining budget, and remaining shares.
    
    Parameters:
    - df: A pandas DataFrame containing the shares and price columns.
    - budget: The initial budget for purchasing shares. If <= 0, the budget is not considered.
    - target_shares: The target number of shares to purchase. If <= 0, the target shares is not considered.
    - cols: The column names for the shares and price.
    - adjust: Whether to adjust the daily shares to not exceed the budget and target shares.
    
    Returns:
    - progress: An updated DataFrame containing the cost, cumulative cost, cumulative shares, remaining budget, and remaining shares.
    """
    # Make sure the DataFrame contains the required columns
    if not all(col in df.columns for col in cols):
        raise ValueError("The DataFrame must contain the required columns")

    # Calculate the cost of purchasing the shares
    # Adjust the daily shares to not exceed the budget and target shares
    if (adjust): # DEBUG: this is a hack to adjust the shares to not exceed the budget and target shares
        remaining_budget = budget
        remaining_shares = target_shares
        # Adjust the daily shares to not exceed the budget and target shares
        for i, row in df.iterrows():
            shares, cost, remaining_budget, remaining_shares = buy_shares(row[cols[0]], row[cols[1]], remaining_budget, remaining_shares)
            df.at[i, cols[0]] = shares # DEBUG: should this become a new column?
            df.at[i, COST_COL] = cost
    else:
        df[COST_COL] = df[cols[0]] * df[cols[1]]

    # Calculate the cumulative cost and shares
    df[CUM_COST_COL] = df[COST_COL].cumsum()
    df[CUM_SHARES_COL] = df[cols[0]].cumsum()

    # Calculate the remaining budget and shares
    if budget > 0:
        df[REM_BUDGET_COL] = budget - df[CUM_COST_COL]
    # TODO: else calculate remaining budget based on shares and price?
    if target_shares > 0:
        df[REM_SHARES_COL] = target_shares - df[CUM_SHARES_COL]
    else:
        df[REM_SHARES_COL] = df[SHARES_COL][::-1].cumsum()[::-1]
        
    # TODO: prevent going negative on budget and shares properly
    df[df < 0] = 0 # DEBUG: this is a hack to set negative values to 0

    return df

def calculate_runtime(df, cols=[SHARES_COL, PRICE_COL, COST_COL], threshold=1):
    """
    Get the runtime and last day of the strategy.
    
    Parameters:
    - df: A pandas DataFrame representing the strategy, containing the cost, cumulative cost, cumulative shares, remaining budget, and remaining shares columns.
    - cols: The column names for the cost, cumulative cost, cumulative shares, remaining budget, and remaining shares.
    - threshold: The threshold for the number of shares purchased to consider the strategy as running.
    
    Returns:
    - total_days: The number of business days the strategy has been running.
    - last_day: A dictionary containing the cost, cumulative cost, cumulative shares, remaining budget, and remaining shares for the last day.
    """
    # Make sure the DataFrame contains the required columns
    #if not all(col in df.columns for col in cols):
    #    raise ValueError("The DataFrame must contain the required columns")
    if not (SHARES_COL in df.columns):
        raise ValueError(f"The DataFrame must contain the required column {SHARES_COL}")

    # Get the last day of the strategy
    is_running = (df[cols[0]] > threshold) # If num shares purchased is greater than threshold
    last_day = df[is_running].last_valid_index()
    total_days = len(df[:last_day].index) # TODO: return?

    return total_days, last_day

def describe(df, cols=[COST_COL, CUM_COST_COL, CUM_SHARES_COL, REM_BUDGET_COL, REM_SHARES_COL]):
    """
    Describe the progress of the strategy over time. Calculates the total cost, total shares, average price, and average shares.
    
    Parameters:
    - df: A pandas DataFrame representing the strategy, containing the cost, cumulative cost, cumulative shares, remaining budget, and remaining shares columns.
    - cols: The column names for the cost, cumulative cost, cumulative shares, remaining budget, and remaining shares.
    
    Returns:
    - description: A dictionary containing the total cost, total shares, average price, and average shares.
    """
    raise NotImplementedError("You should implement this!")
    # Make sure the DataFrame contains the required columns
    if not all(col in df.columns for col in cols):
        raise ValueError("The DataFrame must contain the required columns")

    # Calculate the total cost and shares
    total_cost = df[cols[0]].sum()
    total_shares = df[cols[2]].iloc[-1]

    # Calculate the average price and shares
    average_price = total_cost / total_shares
    average_shares = total_shares / len(df)

    return {
        "total_cost": total_cost,
        "total_shares": total_shares,
        "average_price": average_price,
        "average_shares": average_shares
    }