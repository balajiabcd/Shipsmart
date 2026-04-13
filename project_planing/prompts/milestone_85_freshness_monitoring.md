# Milestone #85: Create Feature Freshness Monitoring

---

## Section 1: Instructions from Previous AI Agent

*(To be filled by Milestone #84 agent)*

---

## Section 2: Detailed Prompt to Finish Milestone

### Task: Track Feature Freshness

**Your Role:** Data Engineer

**Instructions:**
1. Create `src/features/monitor_freshness.py`:
   ```python
   import pandas as pd
   from datetime import datetime, timedelta
   import os
   
   def check_feature_freshness(features_dir='data/features'):
       """Check and report feature freshness"""
       results = []
       
       for file in os.listdir(features_dir):
           if file.endswith('.csv'):
               df = pd.read_csv(f'{features_dir}/{file}')
               # Try to find timestamp columns
               timestamp_cols = [c for c in df.columns if 'time' in c.lower() or 'date' in c.lower()]
               
               if timestamp_cols:
                   latest = pd.to_datetime(df[timestamp_cols[0]]).max()
                   age = datetime.now() - latest
                   results.append({
                       'feature_file': file,
                       'latest_timestamp': latest,
                       'age_hours': age.total_seconds() / 3600
                   })
       
       freshness_df = pd.DataFrame(results)
       freshness_df.to_csv('data/features/freshness_report.csv', index=False)
       
       print("Feature Freshness Report:")
       print(freshness_df)
       
       return freshness_df
   
   if __name__ == '__main__':
       check_feature_freshness()
   ```

2. Create Airflow DAG to run freshness check daily
3. Set up alerts for stale features (>24 hours)
4. Commit

---

## Section 3: Instructions for Next AI Agent

*(Empty)*