#pylint: disable=invalid-name
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def set_date_index(input_df, col_name='Date'):
    """Given a pandas df, parse and set date column to index.
        col_name will be removed and set as datetime index.

    Args:
        input_df (pandas dataframe): Original pandas dataframe
        col_name (string): Name of date column

    Returns:
        pandas dataframe: modified and sorted dataframe
    """
    # Copy df to prevent changing original
    modified_df = input_df.copy()

    # Infer datetime from col and push to month end
    modified_df[col_name] = pd.to_datetime(modified_df[col_name]) \
        + pd.tseries.offsets.MonthEnd(0)

    # Grab month and include as a new column
    modified_df['month'] = modified_df[col_name].dt.month

    # Sort and set index
    modified_df.sort_values(col_name, inplace=True)
    modified_df.set_index(col_name, inplace=True)
    
    # Set as monthly index
    modified_df = modified_df.asfreq('M')

    return modified_df


def get_full_date_range(input_df, col_name='Date'):
    """Get a dataframe with fully padded dates.

    Args:
        input_df (pandas dataframe):
        col_name (str, optional): Defaults to 'Date'.

    Returns:
        pandas dataframe: list of dates from start to end by day
    """
    first_date = np.min(pd.to_datetime(input_df[col_name]))
    last_date = np.max(pd.to_datetime(input_df[col_name]))
    datepad = pd.DataFrame(
        pd.date_range(
            first_date, 
            last_date,
            freq='D'
        )
    )
    datepad.columns = ['Date']
    datepad.sort_values('Date', inplace=True)
    datepad.set_index('Date', inplace=True)
    return datepad


def combine_seasonal_cols(input_df, seasonal_model_results):
    """Adds inplace new seasonal cols to df given seasonal results

    Args:
        input_df (pandas dataframe)
        seasonal_model_results (statsmodels DecomposeResult object)
    """
    # Add results to original df
    input_df['observed'] = seasonal_model_results.observed
    input_df['residual'] = seasonal_model_results.resid
    input_df['seasonal'] = seasonal_model_results.seasonal
    input_df['trend'] = seasonal_model_results.trend

    # NaN to Zero
    cols = ['observed']
    for col in cols:
        input_df[col] = input_df[col].replace(np.nan, 0)


def mround(x, m=5):
    '''Helper method for multiple round'''
    return int(m * round(float(x)/m))


def plot_components(df):
    """Plot data for initial visualization, ultimately visualized in Power BI

    Args:
        df (pandas dataframe)
    """
    df_axis = df.fillna(0)
    ymin = mround(np.min([df_axis.observed, df_axis.trend, df_axis.seasonal, df_axis.residual]),5)
    ymax = mround(np.max([df_axis.observed, df_axis.trend, df_axis.seasonal, df_axis.residual]),5)
    ymin -= 5
    ymax += 5

    plt.figure(figsize=(10,10))

    plt.subplot(4,1,1)
    plt.title("Original Data")
    plt.ylim(ymin, ymax)
    plt.plot(df.index, df.observed)

    plt.subplot(4,1,2)
    plt.title("Trend")
    plt.ylim(ymin, ymax)
    plt.plot(df.index, df.trend)

    plt.subplot(4,1,3)
    plt.title("Seasonal")
    plt.ylim(ymin, ymax)
    plt.plot(df.index, df.seasonal)

    plt.subplot(4,1,4)
    plt.title("Residual")
    plt.ylim(ymin, ymax)
    plt.plot(df.index, df.residual)

    plt.tight_layout(pad=1.0, w_pad=1.0, h_pad=1.0)


def plot_results(df):
    """Plot data for forecast visualization

    Args:
        df (pandas dataframe)
    """
    df_axis = df.fillna(0)
    ymin = mround(np.min([df_axis['Burglary/Breaking and Entering'], df_axis['prediction']]),5)
    ymax = mround(np.max([df_axis['Burglary/Breaking and Entering'], df_axis['prediction']]),5)
    ymin -= 5
    ymax += 5

    plt.figure(figsize=(10,10))

    plt.subplot(1,1,1)
    plt.title("Original Data with Forecast")
    plt.ylim(ymin, ymax)
    plt.plot(df.index, df['Burglary/Breaking and Entering'])
    plt.plot(df.index, df['prediction'])

    plt.tight_layout(pad=1.0, w_pad=1.0, h_pad=1.0)
