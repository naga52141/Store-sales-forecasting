import sys
import json
import pandas as pd
from statsmodels.tsa.statespace.sarimax import SARIMAX
from pmdarima import auto_arima

# ✅ Debugging: Print received arguments
sys.stderr.write(f"Received arguments: {sys.argv}\n")
sys.stderr.flush()

# ✅ Validate input arguments
if len(sys.argv) < 2:
    print(json.dumps({"error": "No CSV file provided"}))
    sys.exit(1)

csv_file = sys.argv[1]

try:
    # ✅ Read CSV and ensure proper data parsing
    df = pd.read_csv(csv_file, parse_dates=['date'], dtype={'sales': float})

    # ✅ Aggregate sales by date
    df = df.groupby('date')['sales'].sum().reset_index()

    # ✅ Train-test split (80% train, 20% test)
    split_date = df['date'].quantile(0.8)
    train_data = df[df['date'] <= split_date]
    test_data = df[df['date'] > split_date]

    if train_data.empty or test_data.empty:
        raise ValueError("Train or test dataset is empty. Check date range.")

    # ✅ Train SARIMA model using auto_arima
    model = auto_arima(
        train_data['sales'],
        start_p=1, start_q=1,
        max_p=3, max_q=3,
        m=3,  # Seasonality (e.g., 3 days)
        start_P=0,
        seasonal=True,
        d=1, D=0,
        trace=False,
        error_action='ignore',
        suppress_warnings=True,
        stepwise=True
    )

    sarima_model = SARIMAX(
        train_data['sales'],
        order=model.order,
        seasonal_order=model.seasonal_order,
        enforce_stationarity=False,
        enforce_invertibility=False
    ).fit(disp=0)

    # ✅ Forecast
    forecast_steps = len(test_data)
    last_train_date = train_data['date'].iloc[-1]  # Last date in training data
    forecast_index = pd.date_range(start=last_train_date, periods=forecast_steps+1)[1:]

    forecast = sarima_model.get_forecast(steps=forecast_steps)
    test_data = test_data.copy()
    test_data['sales_forecast'] = forecast.predicted_mean

    # ✅ Prepare JSON response
    response = {
        "dates": forecast_index.strftime("%Y-%m-%d").tolist(),
        "forecast": forecast.predicted_mean.tolist(),
        "actual_dates": df["date"].dt.strftime("%Y-%m-%d").tolist(),
        "actual_sales": df["sales"].tolist(),
    }

    # ✅ Output JSON
    print(json.dumps(response))

except Exception as e:
    print(json.dumps({"error": str(e)}))
    sys.exit(1)
