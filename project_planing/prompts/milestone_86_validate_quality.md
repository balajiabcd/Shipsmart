# Milestone #86: Validate Feature Quality

---

## Section 1: Instructions from Previous AI Agent

*(To be filled by Milestone #85 agent)*

---

## Section 2: Detailed Prompt to Finish Milestone

### Task: Check Feature Correlations and Distributions

**Your Role:** Data Engineer

**Instructions:**
1. Create `src/features/validate_quality.py`:
   ```python
   import pandas as pd
   import numpy as np
   
   def validate_feature_quality(features_dir='data/features'):
       """Validate feature quality metrics"""
       
       results = []
       
       for file in [f for f in os.listdir(features_dir) if f.endswith('.csv')]:
           df = pd.read_csv(f'{features_dir}/{file}')
           
           results.append({
               'feature_file': file,
               'num_features': len(df.columns),
               'num_rows': len(df),
               'null_pct': df.isnull().sum().sum() / (len(df) * len(df.columns)) * 100,
               'duplicates': df.duplicated().sum()
           })
           
           # Feature correlation with target
           if 'is_delayed' in df.columns:
               corr = df.corr()['is_delayed'].sort_values(ascending=False)
               print(f"\n{file} - Top correlations with target:")
               print(corr.head(10))
       
       quality_df = pd.DataFrame(results)
       quality_df.to_csv('data/features/quality_report.csv', index=False)
       print("\nQuality Report:")
       print(quality_df)
   
   import os
   validate_feature_quality()
   ```

2. Check feature distributions
3. Identify highly correlated features (for removal)
4. Save report to `data/features/quality_report.csv`
5. Commit

---

## Section 3: Instructions for Next AI Agent

*(Empty)*