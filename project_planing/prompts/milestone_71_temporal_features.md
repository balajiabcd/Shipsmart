# Milestone #71: Create Temporal Features

---

## Section 1: Instructions from Previous AI Agent

*(To be filled by Milestone #70 agent)*

---

## Section 2: Detailed Prompt to Finish Milestone

### Task: Create Temporal Features (Hour, Day, Week, Month, Quarter, Year)

**Your Role:** Data Engineer

**Instructions:**
1. Create `src/features/temporal_features.py`:
   ```python
   import pandas as pd
   import numpy as np
   
   def create_temporal_features(df, datetime_col='order_time'):
       """Create temporal features from datetime column"""
       df[datetime_col] = pd.to_datetime(df[datetime_col], errors='coerce')
       
       features = pd.DataFrame()
       
       # Basic temporal features
       features['hour'] = df[datetime_col].dt.hour
       features['day_of_week'] = df[datetime_col].dt.dayofweek
       features['day_of_month'] = df[datetime_col].dt.day
       features['week_of_year'] = df[datetime_col].dt.isocalendar().week
       features['month'] = df[datetime_col].dt.month
       features['quarter'] = df[datetime_col].dt.quarter
       features['year'] = df[datetime_col].dt.year
       
       # Is weekend
       features['is_weekend'] = (features['day_of_week'] >= 5).astype(int)
       
       # Is business hour (9-17)
       features['is_business_hour'] = ((features['hour'] >= 9) & (features['hour'] <= 17)).astype(int)
       
       # Time periods
       features['time_period'] = pd.cut(features['hour'], 
                                       bins=[0, 6, 12, 18, 24],
                                       labels=['night', 'morning', 'afternoon', 'evening'])
       
       return features
   
   if __name__ == '__main__':
       orders = pd.read_csv('data/processed/orders.csv')
       temporal = create_temporal_features(orders)
       temporal.to_csv('data/features/temporal_features.csv', index=False)
       print(f"Created temporal features: {temporal.shape}")
   ```

2. Run and save to `data/features/temporal_features.csv`
3. Commit

---

## Section 3: Instructions for Next AI Agent

*(Empty - To be filled by this agent after completion)*