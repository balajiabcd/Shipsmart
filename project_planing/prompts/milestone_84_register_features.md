# Milestone #84: Register Features in Feast

---

## Section 1: Instructions from Previous AI Agent

*(To be filled by Milestone #83 agent)*

---

## Section 2: Detailed Prompt to Finish Milestone

### Task: Register All Features in Feast

**Your Role:** Data Engineer

**Instructions:**
1. Create feature definitions for each feature set:
   ```python
   # feature_repo/features/temporal.py
   from feast import Feature, FeatureView, FileSource
   
   temporal_source = FileSource(
       path="data/features/temporal_features.csv",
       timestamp_field="timestamp"
   )
   
   temporal_features = [
       Feature(name="hour", dtype=Int64),
       Feature(name="day_of_week", dtype=Int64),
       Feature(name="is_weekend", dtype=Int64),
       # ... more features
   ]
   ```

2. Repeat for all feature files:
   - temporal_features.py
   - distance_features.py
   - weather_features.py
   - driver_features.py
   - etc.

3. Run `feast apply` to register all features

4. Commit

---

## Section 3: Instructions for Next AI Agent

*(Empty)*