# Milestone #23: Validate All Raw CSVs

---

## Section 1: Instructions from Previous AI Agent

*(To be filled by Milestone #22 agent)*

---

## Section 2: Detailed Prompt to Finish Milestone

### Task: Validate All Raw CSVs and Document Issues

**Your Role:** Data Engineer

**Instructions:**
1. Create `src/data_simulation/validate_data.py` to validate all 22 CSV files:
   - Check for missing values per column
   - Check for duplicates
   - Check for outliers
   - Check for data type consistency
   - Check for referential integrity

2. Create validation report `docs/data_quality_report.md` documenting:
   - Summary of each file
   - Issues found per file
   - Data quality score per file

3. Example validation code:
   ```python
   import pandas as pd
   import os
   
   files = ['orders.csv', 'drivers.csv', ...]
   report = {}
   
   for f in files:
       df = pd.read_csv(f'data/raw/{f}')
       report[f] = {
           'rows': len(df),
           'columns': len(df.columns),
           'missing_pct': df.isnull().sum().sum() / (len(df) * len(df.columns)) * 100,
           'duplicates': df.duplicated().sum()
       }
   
   # Save report
   ```

4. Commit and push

---

### Milestone #23 Completed
- validate_data.py script
- docs/data_quality_report.md
- 18 files validated, 98.7% avg quality
- Next: Milestone #24