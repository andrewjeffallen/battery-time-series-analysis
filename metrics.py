import numpy as np 
import pandas as pd 

def _root_mean_squared_error(y_true, y_pred):
    result = np.sqrt(np.mean((y_true - y_pred) ** 2))
    return np.round(result, 3)


def _mean_absolute_error(y_true, y_pred):
    result = np.mean(np.abs(y_true - y_pred))
    return np.round(result, 3)


def _mean_absolute_percentage_error(y_true, y_pred):
    y_true, y_pred = np.array(y_true), np.array(y_pred)
    return np.round(np.mean(np.abs((y_true - y_pred) / y_true)) * 100, 3)


def _mean_square_error(y_true, y_pred):
    MSE = np.square(np.subtract(y_true, y_pred)).mean()
    return np.round(MSE, 3)



def calculate_metrics(df, actual, predicted):
    mape = _mean_absolute_percentage_error(df[actual], df[predicted])
    rmse = _root_mean_squared_error(df[actual], df[predicted])
    mae = _mean_absolute_error(df[actual], df[predicted])
    mse = _mean_square_error(df[actual], df[predicted])
    forecast = predicted
    metrics_df = pd.DataFrame(
        {
            "RMSE": rmse,
            "MAPE": mape,
            "MAE": mae,
            "MSE": mse,
        },
        index=[0],
    )
    return metrics_df