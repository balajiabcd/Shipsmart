# Milestone #69: Merge External Data with Simulated

---

## Section 1: Instructions from Previous AI Agent

*(To be filled by Milestone #68 agent)*

---

## Section 2: Detailed Prompt to Finish Milestone

### Task: Combine External API Data with Simulated Data

**Your Role:** Data Engineer

**Instructions:**
1. Create `src/data_engineering/merge_external_data.py`:
   ```python
   import pandas as pd
   from datetime import datetime
   
   def merge_external_with_simulated():
       # Load simulated weather data
       weather_sim = pd.read_csv('data/raw/weather.csv')
       
       # Fetch real weather for major cities
       from src.external_apis.weather_api import WeatherAPI
       weather_api = WeatherAPI()
       
       real_weather = []
       for city in ['Berlin', 'Munich', 'Hamburg', 'Frankfurt']:
           data = weather_api.get_current_weather(city)
           if data:
               real_weather.append({
                   'city': city,
                   'temperature': data['main']['temp'],
                   'condition': data['weather'][0]['main'],
                   'timestamp': datetime.now()
               })
       
       # Create enriched dataset
       weather_df = pd.DataFrame(real_weather)
       
       # Merge with simulated
       merged = pd.merge(
           weather_sim[weather_sim['location_id'].isin(['BER', 'MUN', 'HAM', 'FRA'])],
           weather_df,
           left_on='location_id',
           right_on='city',
           how='left',
           suffixes=('_sim', '_real')
       )
       
       # Save enriched data
       merged.to_csv('data/processed/weather_enriched.csv', index=False)
       print(f"Merged {len(merged)} records")
   
   merge_external_with_simulated()
   ```

2. Repeat for traffic and holidays
3. Create Airflow DAG to run merge periodically
4. Commit

---

## Section 3: Instructions for Next AI Agent

*(Empty)*