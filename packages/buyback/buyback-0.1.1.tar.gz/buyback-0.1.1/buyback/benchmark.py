import numpy as np

from .constants import *

def calculate_vwap(price, volume): # DEBUG: insitutional is a misnomer
    """
    Calculate the Volume Weighted Average Price (VWAP)

    Parameters:
        price (array): The price of the asset
        volume (array): The volume of the asset

    Returns:
        vwap_values (array): The vwap values at each point in time
    """
    #vwap_values = np.cumsum((price * volume).replace(0, np.nan)) / np.cumsum(volume)
    vwap_values = np.cumsum(price * volume) / np.cumsum(volume)

    return vwap_values

def calculate_bogus_benchmark(price, volume=None): # DEBUG: check if this is correct
    """
    Calculate the bogus Volume Weighted Average Price (VWAP)

    Parameters:
        price (array): The price of the asset
        volume (array): The volume of the asset

    Returns:
        vwap_values (array): The vwap values at each point in time
    """
    #vwap_values = (price * volume) / (volume)
    vwap_values = price.expanding().mean() # assuming price is the day's average purchase price
    return vwap_values

def calculate_typical_price(high=None, low=None, close=None, df=None, cols=[HIGH_COL, LOW_COL, CLOSE_COL]):
    """
    Calculate the typical price of an asset

    Parameters:
        high (pd.Series): The high price of the asset
        low (pd.Series): The low price of the asset
        close (pd.Series): The close price of the asset
        df (pd.DataFrame): The dataframe containing the high, low, and close prices
        cols (list): The column names for the high, low, and close prices

    Returns:
        typical_price (pd.Series): The typical price of the asset
    """

    if df is not None:
        high = df[cols[0]]
        low = df[cols[1]]
        close = df[cols[2]]
        # TODO: insert in the dataframe?

    typical_price = (high + low + close) / 3
    return typical_price