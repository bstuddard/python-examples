# Libraries
import pandas as pd
import numpy as np
from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.tsa.statespace.sarimax import SARIMAX

# Local Imports
from helpers import set_date_index, combine_seasonal_cols, plot_components, plot_results


# Data Load: Read in, adjust for days in month, set date index
df = pd.read_csv("../data/Kansas_City_Crime__NIBRS__Summary.csv")
df = df[['Date', 'Burglary/Breaking and Entering']]
df['Burglary/Breaking and Entering'] = \
    df['Burglary/Breaking and Entering'] \
        / pd.to_datetime(df['Date']).dt.day
df = set_date_index(df, 'Date')

# Train/Test Split
df_train = df[:-12].copy()
df_test = df[-12:].copy()

# Seasonal decompose
sd = seasonal_decompose(df_train['Burglary/Breaking and Entering'], period=12)
combine_seasonal_cols(df_train, sd)

# Plot for initial inspection
plot_components(df_train)

# Trend and Residual combination
df_train['trend_plus_resid'] = df_train['trend'] + df_train['residual']
df_train = df_train[df_train.trend_plus_resid.notnull()]

# Save results at this step
df_train.to_csv("../data/prelim_data.csv")

# Sarimax
sm = SARIMAX(df_train.trend_plus_resid, order=(1,0,0)) # to be tuned/optimized in a future article
res = sm.fit()
res.summary()

# Make trend forecast
df_test['trend_prediction'] = res.predict(start=np.min(df_test.index), end=np.max(df_test.index))

# Add Seasonal component
seasonal_prediction = df_train[-12:].reset_index()[['month', 'seasonal']]
df_test = df_test.reset_index().merge(seasonal_prediction, how='left', left_on='month', right_on='month').set_index('Date')
df_test['combined_prediction'] = df_test['trend_prediction'] + df_test['seasonal']

# Add to orignal df for visualization
df['prediction'] = df_test['combined_prediction']

# Plot comparison
plot_results(df)

# Save final_results
df.to_csv("../data/final_results.csv")
