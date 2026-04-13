# Milestone #73: Create Weather Severity Index

---

## Section 1: Instructions from Previous AI Agent

*(To be filled by Milestone #72 agent)*

---

## Section 2: Detailed Prompt to Finish Milestone

### Task: Combine Weather Conditions into Severity Score

**Your Role:** Data Engineer

**Instructions:**
1. Create `src/features/weather_features.py`:
   ```python
   import pandas as pd
   import numpy as np
   
   def create_weather_severity(weather_df):
       """Create weather severity index"""
       features = pd.DataFrame()
       
       # Temperature severity (extreme temps are bad)
       features['temp_severity'] = np.where(
           (weather_df['temperature'] < 0) | (weather_df['temperature'] > 35), 3,
           np.where((weather_df['temperature'] < 5) | (weather_df['temperature'] > 30), 2, 1)
       )
       
       # Condition severity
       condition_map = {
           'clear': 0, 'cloudy': 1, 'fog': 2, 'rain': 3, 'snow': 4, 'storm': 5
       }
       features['condition_severity'] = weather_df['condition'].map(condition_map).fillna(1)
       
       # Wind severity
       features['wind_severity'] = pd.cut(
           weather_df['wind_speed'],
           bins=[0, 10, 20, 30, float('inf')],
           labels=[0, 1, 2, 3]
       ).astype(float).fillna(0)
       
       # Combined severity
       features['weather_severity_index'] = (
           features['temp_severity'] + 
           features['condition_severity'] + 
           features['wind_severity']
       )
       
       return features
   ```

2. Process weather data and create severity index
3. Save to `data/features/weather_features.csv`
4. Commit

---

## Section 3: Instructions for Next AI Agent

*(Empty)*