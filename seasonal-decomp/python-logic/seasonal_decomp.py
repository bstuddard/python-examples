# Libraries
import pandas as pd
from statsmodels.tsa.seasonal import seasonal_decompose

# Local Imports
from helpers import set_date_index, combine_seasonal_cols, plot_components


# Data Load: Read in, adjust for days in month, set date index
df = pd.read_csv("../data/Kansas_City_Crime__NIBRS__Summary.csv") # https://data.kcmo.org/dataset/Kansas-City-Crime-NIBRS-Summary/6wc4-sd7p
df = df[['Date', 'Burglary/Breaking and Entering']]
df['Burglary/Breaking and Entering'] = \
    df['Burglary/Breaking and Entering'] \
        / pd.to_datetime(df['Date']).dt.day
df = set_date_index(df, 'Date')

# Seasonal decompose
sd = seasonal_decompose(df, period=12)
combine_seasonal_cols(df, sd)

# Plot and output results
plot_components(df)
df.to_csv("../data/results.csv")
