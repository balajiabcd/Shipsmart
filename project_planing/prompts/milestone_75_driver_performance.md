# Milestone #75: Create Driver Performance Score

---

## Section 1: Instructions from Previous AI Agent

*(To be filled by Milestone #74 agent)*

---

## Section 2: Detailed Prompt to Finish Milestone

### Task: Calculate Driver Performance from Historical Data

**Your Role:** Data Engineer

**Instructions:**
1. Create `src/features/driver_features.py`:
   ```python
   import pandas as pd
   
   def create_driver_scores(drivers_perf_df):
       # Average on-time rate
       on_time_rate = drivers_perf_df.groupby('driver_id').apply(
           lambda x: x['on_time_count'].sum() / x['total_deliveries'].sum() * 100
       )
       
       # Average rating
       avg_rating = drivers_perf_df.groupby('driver_id')['rating'].mean()
       
       # Recent performance (last 30 days)
       recent = drivers_perf_df.tail(30)
       recent_perf = recent.groupby('driver_id')['rating'].mean()
       
       driver_scores = pd.DataFrame({
           'driver_id': on_time_rate.index,
           'on_time_rate': on_time_rate.values,
           'avg_rating': avg_rating.values,
           'recent_rating': [recent_perf.get(d, avg_rating[d]) for d in on_time_rate.index]
       })
       
       # Composite score
       driver_scores['performance_score'] = (
           driver_scores['on_time_rate'] * 0.4 +
           driver_scores['avg_rating'] * 20 * 0.3 +
           driver_scores['recent_rating'] * 20 * 0.3
       )
       
       return driver_scores
   ```

2. Process and save to `data/features/driver_scores.csv`
3. Commit

---

## Section 3: Instructions for Next AI Agent

*(Empty)*