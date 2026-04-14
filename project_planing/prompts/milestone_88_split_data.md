# Milestone #88: Split Data (Train/Test/Val)

---

## Section 1: Instructions from Previous AI Agent

Milestone 87 complete. Feature engineering documentation created.

---

## Section 3: Instructions for Next AI Agent

Milestone 88 complete. Created:
- src/ml_models/split_data.py

Features:
- load_features_and_target()
- split_data() - stratified train/val/test split
- save_splits() - save to CSV
- get_split_statistics()
- create_time_series_split()
- create_stratified_kfold()

Default: 70% train, 15% val, 15% test

Continue with Milestone 89: Train Logistic Regression