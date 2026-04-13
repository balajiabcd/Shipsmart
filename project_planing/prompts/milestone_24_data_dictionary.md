# Milestone #24: Create Data Dictionary

---

## Section 1: Instructions from Previous AI Agent

*(To be filled by Milestone #23 agent)*

---

## Section 2: Detailed Prompt to Finish Milestone

### Task: Create Data Dictionary Documenting All Columns

**Your Role:** Data Engineer

**Instructions:**
1. Create `docs/data_dictionary.md` with:
   - For each CSV file:
     - File name and description
     - Column name
     - Data type (string, int, float, datetime)
     - Description
     - Sample values
     - Valid range/values

2. Example format:
   ```markdown
   ## orders.csv
   
   | Column | Type | Description | Sample |
   |--------|------|-------------|--------|
   | order_id | string | Unique order identifier | ORD-00000001 |
   | customer_id | string | FK to customers | CUST-000001 |
   ...
   ```

3. Cover all 22 CSV files
4. Commit and push

---

### Milestone #24 Completed
- docs/data_dictionary.md
- Documented all 18 CSV files with columns, types, samples
- Next: Milestone #25