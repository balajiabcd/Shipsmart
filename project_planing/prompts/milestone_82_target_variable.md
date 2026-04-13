# Milestone #82: Create Target Variable

---

## Section 1: Instructions from Previous AI Agent

*(To be filled by Milestone #81 agent)*

---

## Section 2: Detailed Prompt to Finish Milestone

### Task: Define Delay (Yes/No) and delay_minutes

**Your Role:** ML Engineer 1

**Instructions:**
1. Create `src/features/create_target.py`:
   ```python
   import pandas as pd
   import numpy as np
   
   def create_target_variable(orders_df):
       """Create target variables for ML models"""
       
       # Calculate delay in minutes
       orders_df['delivery_promise'] = pd.to_datetime(orders_df['delivery_promise'])
       orders_df['actual_delivery'] = pd.to_datetime(orders_df['actual_delivery'])
       
       # Delay in minutes
       delay_minutes = (orders_df['actual_delivery'] - orders_df['delivery_promise']).dt.total_seconds() / 60
       
       # Binary target: 1 if delayed (>0 minutes), 0 otherwise
       is_delayed = (delay_minutes > 0).astype(int)
       
       # For pending/in-transit orders, we don't know yet - will predict
       is_delayed = is_delayed.fillna(-1)  # -1 for unknown
       
       target_df = pd.DataFrame({
           'order_id': orders_df['order_id'],
           'is_delayed': is_delayed,  # 1=delayed, 0=on_time, -1=unknown
           'delay_minutes': delay_minutes.fillna(0),  # 0 for non-delivered
           'delay_minutes_actual': delay_minutes  # actual for delivered, None for pending
       })
       
       print(f"Target distribution:")
       print(target_df['is_delayed'].value_counts())
       
       return target_df
   
   if __name__ == '__main__':
       orders = pd.read_csv('data/processed/orders.csv')
       targets = create_target_variable(orders)
       targets.to_csv('data/features/target.csv', index=False)
   ```

2. Run and save to `data/features/target.csv`
3. Document the target variable in `docs/target_variable.md`
4. Commit

**Note:** This defines the target for classification (is_delayed) and regression (delay_minutes) models.

---

## Section 3: Instructions for Next AI Agent

*(Empty)*