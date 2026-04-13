# Milestone #232: Set Up Time-Series Pipeline

**Your Role:** AI/LLM Engineer

Prepare temporal data:

```python
# src/anomaly/time_series_pipeline.py

import pandas as pd
import numpy as np
from datetime import datetime, timedelta

class TimeSeriesPipeline:
    def __init__(self):
        self.data = None
    
    def load_delivery_data(self, start_date: datetime, end_date: datetime) -> pd.DataFrame:
        # Load delivery events with timestamps
        df = pd.read_csv('data/delivery_events.csv')
        
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df = df[(df['timestamp'] >= start_date) & (df['timestamp'] <= end_date)]
        
        return df
    
    def aggregate_metrics(self, df: pd.DataFrame, freq: str = 'H') -> pd.DataFrame:
        df = df.set_index('timestamp')
        
        metrics = pd.DataFrame()
        metrics['delivery_count'] = df.resample(freq).size()
        metrics['avg_delay'] = df['delay_minutes'].resample(freq).mean()
        metrics['delay_rate'] = df['is_delayed'].resample(freq).mean()
        metrics['driver_count'] = df['driver_id'].resample(freq).nunique()
        
        return metrics.fillna(0)
    
    def create_lag_features(self, df: pd.DataFrame, lags: list = [1, 2, 4, 8, 24]) -> pd.DataFrame:
        for lag in lags:
            df[f'lag_{lag}h'] = df['delay_rate'].shift(lag)
        
        df['rolling_mean_4h'] = df['delay_rate'].rolling(window=4).mean()
        df['rolling_std_4h'] = df['delay_rate'].rolling(window=4).std()
        df['rolling_mean_24h'] = df['delay_rate'].rolling(window=24).mean()
        
        return df.dropna()
    
    def prepare_for_detection(self, df: pd.DataFrame, target_column: str = 'delay_rate') -> tuple:
        X = df.drop(columns=[target_column])
        y = df[target_column]
        
        return X, y
```

Commit.