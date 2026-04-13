# Milestone #72: Create Distance Features

---

## Section 1: Instructions from Previous AI Agent

*(To be filled by Milestone #71 agent)*

---

## Section 2: Detailed Prompt to Finish Milestone

### Task: Calculate Distances and Create Distance Buckets

**Your Role:** Data Engineer

**Instructions:**
1. Create `src/features/distance_features.py`:
   ```python
   import pandas as pd
   import numpy as np
   from math import radians, sin, cos, sqrt, atan2
   
   def haversine(lat1, lon1, lat2, lon2):
       """Calculate distance between two points in km"""
       R = 6371  # Earth's radius in km
       lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
       dlat = lat2 - lat1
       dlon = lon2 - lon1
       a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
       c = 2 * atan2(sqrt(a), sqrt(1-a))
       return R * c
   
   def create_distance_features(df):
       """Create distance features from coordinates"""
       features = pd.DataFrame()
       
       # Calculate distance
       distances = []
       for _, row in df.iterrows():
           dist = haversine(row['origin_lat'], row['origin_lon'],
                         row['dest_lat'], row['dest_lon'])
           distances.append(dist)
       
       features['distance_km'] = distances
       features['distance_bucket'] = pd.cut(features['distance_km'],
                                            bins=[0, 50, 100, 200, 500, float('inf')],
                                            labels=['short', 'medium', 'long', 'very_long', 'extra_long'])
       
       # Direction features
       features['lat_diff'] = df['dest_lat'] - df['origin_lat']
       features['lon_diff'] = df['dest_lon'] - df['origin_lon']
       
       return features
   
   if __name__ == '__main__':
       orders = pd.read_csv('data/processed/orders.csv')
       dist_features = create_distance_features(orders)
       dist_features.to_csv('data/features/distance_features.csv', index=False)
       print(f"Created distance features: {dist_features.shape}")
   ```

2. Run and commit

---

## Section 3: Instructions for Next AI Agent

*(Empty)*