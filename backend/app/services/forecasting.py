import pandas as pd
from prophet import Prophet

def predict_demand(sales_data: list[dict], periods: int = 30) -> list[dict]:
    """
    Takes historical sales data [{"date": "2026-01-01", "units_sold": 15}, ...]
    and returns a future demand forecast using Facebook Prophet.
    """
    if not sales_data or len(sales_data) < 2:
        raise ValueError("Insufficient sales history for forecasting. At least 2 data points are required.")

    # 1. Convert historical data into a Pandas DataFrame
    df = pd.DataFrame(sales_data)
    
    # Prophet requires columns: 'ds' (datestamp) and 'y' (value to forecast)
    df = df.rename(columns={"date": "ds", "units_sold": "y"})
    df['ds'] = pd.to_datetime(df['ds'])

    # 2. Initialize and fit the Prophet model
    model = Prophet(weekly_seasonality=True, daily_seasonality=False, yearly_seasonality=False)
    model.fit(df)

    # 3. Create a future dataframe for predictions
    future = model.make_future_dataframe(periods=periods)
    
    # 4. Generate forecast
    forecast = model.predict(future)

    # 5. Format results (filter out negative predictions since sales can't be negative)
    result_df = forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail(periods)
    result_df['yhat'] = result_df['yhat'].clip(lower=0).round().astype(int)
    result_df['yhat_lower'] = result_df['yhat_lower'].clip(lower=0).round().astype(int)
    result_df['yhat_upper'] = result_df['yhat_upper'].clip(lower=0).round().astype(int)

    # Convert back to list of dictionaries
    forecast_list = []
    for _, row in result_df.iterrows():
        forecast_list.append({
            "date": row['ds'].strftime('%Y-%m-%d'),
            "predicted_units": int(row['yhat']),
            "lower_bound": int(row['yhat_lower']),
            "upper_bound": int(row['yhat_upper'])
        })

    return forecast_list