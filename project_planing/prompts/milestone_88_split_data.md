# Milestone #88: Split Data (Train/Test/Val)

---

## Section 1: Instructions from Previous AI Agent

*(To be filled by Milestone #87 agent)*

---

## Section 2: Detailed Prompt to Finish Milestone

### Task: Create Train/Test/Validation Data Splits

**Your Role:** ML Engineer 1

**Instructions:**
1. Create `src/ml_models/split_data.py`:
   ```python
   import pandas as pd
   import numpy as np
   from sklearn.model_selection import train_test_split
   
   def load_and_split_data():
       # Load features and target
       features = pd.read_csv('data/features/all_features.csv')
       target = pd.read_csv('data/features/target.csv')
       
       # Merge features and target
       df = features.merge(target, on='order_id')
       
       # Remove unknown target values (pending orders)
       df = df[df['is_delayed'] != -1]
       
       # Split: 70% train, 15% validation, 15% test
       X = df.drop(['order_id', 'is_delayed', 'delay_minutes'], axis=1)
       y_class = df['is_delayed']
       y_reg = df['delay_minutes']
       
       # First split: train vs temp
       X_train, X_temp, y_train_class, y_temp_class = train_test_split(
           X, y_class, test_size=0.3, random_state=42, stratify=y_class
       )
       
       # Second split: val vs test
       X_val, X_test, y_val_class, y_test_class = train_test_split(
           X_temp, y_temp_class, test_size=0.5, random_state=42, stratify=y_temp_class
       )
       
       # Save splits
       X_train.to_csv('data/ml/train_features.csv', index=False)
       X_val.to_csv('data/ml/val_features.csv', index=False)
       X_test.to_csv('data/ml/test_features.csv', index=False)
       
       y_train_class.to_csv('data/ml/train_target_class.csv', index=False)
       y_val_class.to_csv('data/ml/val_target_class.csv', index=False)
       y_test_class.to_csv('data/ml/test_target_class.csv', index=False)
       
       print(f"Train: {len(X_train)}, Val: {len(X_val)}, Test: {len(X_test)}")
       print(f"Class distribution (train): {y_train_class.value_counts().to_dict()}")
   
   load_and_split_data()
   ```

2. Create data directories
3. Run and save splits
4. Commit

---

## Section 3: Instructions for Next AI Agent

*(Empty - To be filled by this agent after completion)*