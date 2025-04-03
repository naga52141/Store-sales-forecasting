import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from prophet import Prophet

st.set_page_config(page_title='Prophet Forecast', page_icon="🔮")

with st.sidebar:
    st.markdown("# Hello again 👋")
    st.markdown("# This page shows the sales forecasts for the Favorita Grocery Store using Facebook Prophet model to predict sales from 2017-01-01 to 2017-08-15.")
    st.markdown("# Train data for the forecasts is from 2013-01-08 to 2016-12-31.")

# Define a function to load data
@st.cache
def load_data():
    df = pd.read_csv("/Users/alapakanagajaswanth/Desktop/Store-Sales-Forecasting-main/data/store_sales_raw.csv")  # Ensure the path is correct
    return df

# Define a function to preprocess data and aggregate by date
def aggregate(df):
    # Aggregate sales by date using sum
    date_total_sales = df.groupby('date')['sales'].sum().reset_index()
    # Convert the 'date' column to datetime
    date_total_sales['date'] = pd.to_datetime(date_total_sales['date'])
    return date_total_sales

# Define a function to perform train-test split
def train_test_split(date_total_sales, split_date):
    # Ensure split_date is a datetime object
    if not isinstance(split_date, pd.Timestamp):
        split_date = pd.to_datetime(split_date)
    
    # Perform the split
    train_data = date_total_sales.loc[date_total_sales['date'] <= split_date]
    test_data = date_total_sales.loc[date_total_sales['date'] > split_date]
    return train_data, test_data

# Function to preprocess the input data for Prophet
def preprocess_data(data, column_names={'date': 'ds', 'sales': 'y'}):
    df = data.copy()
    df.reset_index(inplace=True)
    df.rename(columns=column_names, inplace=True)
    return df

# Function to train the Prophet model
def train_prophet_model(data):
    model = Prophet()
    model.fit(data)
    return model

# Function to make forecasts with the Prophet model
def forecast_prophet_model(model, future_dates):
    forecast = model.predict(future_dates)
    return forecast

# Function to plot the forecast
def plot_forecast(model, forecast):
    fig1 = model.plot(forecast)
    plt.ticklabel_format(style='plain', axis='y')
    st.pyplot(fig1)

    fig2 = model.plot_components(forecast)
    plt.ticklabel_format(style='plain', axis='y')
    st.pyplot(fig2)

# Load and preprocess the data
store_sales_df = load_data()
date_total_sales = aggregate(store_sales_df)

# Splitting the data into train and test sets
split_date = st.sidebar.date_input('Train-test split date', value=pd.to_datetime('2016-12-31'))
train_data, test_data = train_test_split(date_total_sales, split_date)

# Preprocess the data
train_prophet = preprocess_data(train_data)
test_prophet = preprocess_data(test_data)

# User triggers the forecast generation
if st.button('Get the Prophet forecast'):
    # Train the model automatically
    prophet_model = train_prophet_model(train_prophet)

    # Forecasting
    future_dates = pd.DataFrame({'ds': test_prophet['ds']})
    forecast = forecast_prophet_model(prophet_model, future_dates)

    # Plotting the forecast
    plot_forecast(prophet_model, forecast)

    # Process forecasted data for display
    # Rename 'ds' to 'date' and 'yhat' to 'sales_pred'
    forecast.rename(columns={'ds': 'date', 'yhat': 'sales_pred'}, inplace=True)

    # Add actual sales data to the forecast DataFrame
    forecast['sales_actual'] = test_prophet['y'].values

    # Set 'date' as the index
    forecast.set_index('date', inplace=True)

    # Display the forecast DataFrame
    st.write(forecast[['sales_pred', 'sales_actual']])

    # Plot actual vs forecast
    st.line_chart(forecast[['sales_actual', 'sales_pred']])