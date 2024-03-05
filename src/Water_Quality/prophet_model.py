# -*- coding: utf-8 -*-
"""prophet_model.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1Iht0ReFsIGVCiPZ__JM4OLDxztGbL6Kj
"""

from google.colab import drive
drive.mount('/content/drive/')

import pickle

from prophet import Prophet
from sklearn.metrics import mean_absolute_error, mean_squared_error

import pandas as pd
import numpy as np

file_path = 'water_merged.csv'

df = pd.read_csv(file_path)

filtered_df = df1[df1['county'] == 'Cass']

#filtered_df = filtered_df.drop(['date_site', 'gauge_height','lake_wsl', 'stream_wsl', 'Locationdep', 'Countyname'], axis=1)

print(len(filtered_df))
filtered_df.dropna(subset=['Streamflow'], inplace=True)
print(len(filtered_df))

df = filtered_df

# Ensure 'date' is of datetime type
df['date'] = pd.to_datetime(df['date'])

# Placeholder for storing evaluation metrics
evaluation_metrics = {}

# Correctly iterate over each unique site_no
for site in df['site_no'].unique():
    # Filter the DataFrame for the current site_no
    site_df = df[df['site_no'] == site].copy()

    # Rename columns as required by Prophet
    site_df.rename(columns={'date': 'ds', 'Streamflow': 'y'}, inplace=True)

    # Initialize and fit the Prophet model
    model = Prophet()
    model.fit(site_df[['ds', 'y']])

    # Make future DataFrame for predictions
    future = model.make_future_dataframe(periods=0)  # Adjust periods for actual forecasting

    # Predict
    forecast = model.predict(future)

    # Compare predictions with the actual values
    y_true = site_df['y'].values
    y_pred = forecast['yhat'].values

    # Calculate metrics
    mae = mean_absolute_error(y_true, y_pred)
    mse = mean_squared_error(y_true, y_pred)
    rmse = np.sqrt(mse)

    # Store metrics for each site
    evaluation_metrics[site] = {'MAE': mae, 'MSE': mse, 'RMSE': rmse}

# Print evaluation metrics for each site
for site, metrics in evaluation_metrics.items():
    print(f"Site: {site}, Metrics: {metrics}")

# Ensure 'date' is of datetime type
df['date'] = pd.to_datetime(df['date'])

# Placeholder for storing forecasts
forecasts = {}

# Correctly iterate over each unique site_no
for site in df['site_no'].unique():
    # Filter the DataFrame for the current site_no
    site_df = df[df['site_no'] == site].copy()

    # Rename columns as required by Prophet
    site_df = site_df.rename(columns={'date': 'ds', 'Streamflow': 'y'})

    # Initialize and fit the Prophet model
    model = Prophet()
    model.fit(site_df[['ds', 'y']])

    # Make future DataFrame for predictions, adjust periods to forecast the next 3 months
    future = model.make_future_dataframe(periods=90)

    # Predict
    forecast = model.predict(future)

    # Optionally, store the entire forecast DataFrame for later use or inspection
    forecasts[site] = forecast

# Preparing the final DataFrame
final_forecasts = []  # List to hold DataFrames for each site

for site, forecast in forecasts.items():
    # Select relevant columns
    site_forecast = forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].copy()

    # Add a 'site' column with the site number
    site_forecast['site'] = site

    # Append the site forecast to the list
    final_forecasts.append(site_forecast)

# Concatenate all site forecasts into a single DataFrame
final_df = pd.concat(final_forecasts, ignore_index=True)

# Reorder the DataFrame columns as specified
final_df = final_df[['ds', 'site', 'yhat', 'yhat_lower', 'yhat_upper']]

# Display the first few rows of the final DataFrame to verify the output
print(final_df.head())

# Save the model to disk
with open(f'model_{site}.pkl', 'wb') as f:
    pickle.dump(model, f)

from sklearn.preprocessing import MinMaxScaler

# Ensure 'date' is of datetime type
df['date'] = pd.to_datetime(df['date'])

# Placeholder for storing forecasts
forecasts = {}

# Initialize the scaler
scaler = MinMaxScaler(feature_range=(0, 1))

# The forecast should start from 2024-02-01
start_date = pd.Timestamp('2024-02-01')

# Create a DataFrame for the future dates starting from start_date for the next 90 days
future_dates = pd.date_range(start=start_date, periods=90, freq='D')
future_df = pd.DataFrame({'ds': future_dates})

# Iterate over each unique site_no
for site in df['site_no'].unique():
    # Filter the DataFrame for the current site_no
    site_df = df[df['site_no'] == site].copy()

    # Normalize the 'Streamflow' values
    site_df['normalized'] = scaler.fit_transform(site_df[['Streamflow']])

    # Rename columns as required by Prophet
    site_df_renamed = site_df.rename(columns={'date': 'ds', 'normalized': 'y'})

    # Initialize and fit the Prophet model
    model = Prophet( growth='linear',
    daily_seasonality=False,
    weekly_seasonality=True,
    yearly_seasonality=False,
    seasonality_mode='multiplicative')
    model.fit(site_df_renamed[['ds', 'y']])

    # Predict using the manually created future DataFrame
    forecast = model.predict(future_df)

    # Denormalize the forecasted values
    forecast[['yhat', 'yhat_lower', 'yhat_upper']] = scaler.inverse_transform(
        forecast[['yhat', 'yhat_lower', 'yhat_upper']])

    # Ensure all yhat values are 0 or above
    forecast['yhat'] = forecast['yhat'].clip(lower=0)
    forecast['yhat_lower'] = forecast['yhat_lower'].clip(lower=0)
    forecast['yhat_upper'] = forecast['yhat_upper'].clip(lower=0)

    # Add a 'site' column to the forecast for identification
    forecast['site'] = site

    # Store the forecast
    forecasts[site] = forecast

# Combine all individual forecasts into a final DataFrame
final_forecasts = pd.concat([forecasts[site] for site in forecasts])

# Select and reorder the desired columns
final_df = final_forecasts[['ds', 'site', 'yhat', 'yhat_lower', 'yhat_upper']]

# Display the first few rows of the final DataFrame
print(final_df.head())

final_df.to_csv('fbprophet_pred.csv', index=False)