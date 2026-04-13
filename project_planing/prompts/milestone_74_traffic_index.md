# Milestone #74: Create Traffic Index

---

## Section 1: Instructions from Previous AI Agent

*(To be filled by Milestone #73 agent)*

---

## Section 2: Detailed Prompt to Finish Milestone

### Task: Create Traffic Congestion Score

**Your Role:** Data Engineer

**Instructions:**
1. Create traffic index from `traffic` table:
   ```python
   import pandas as pd
   import numpy as np
   
   def create_traffic_index(traffic_df):
       features = pd.DataFrame()
       
       # Average congestion level per route/time
       features['avg_congestion'] = traffic_df.groupby('route_id')['congestion_level'].transform('mean')
       
       # Peak hour traffic (7-9 AM, 5-7 PM)
       features['is_peak_hour'] = traffic_df['hour'].isin([7,8,9,17,18,19]).astype(int)
       
       # Rush hour congestion score
       features['rush_hour_index'] = features['avg_congestion'] * (1 + features['is_peak_hour'])
       
       return features
   ```

2. Create from traffic data
3. Save to `data/features/traffic_features.csv`
4. Commit

---

## Section 3: Instructions for Next AI Agent

*(Empty)*