# Milestone #8: Generate Warehouses CSV (Unclean)

---

## Section 1: Instructions from Previous AI Agent

*(To be filled by Milestone #7 agent)*

---

## Section 2: Detailed Prompt to Finish Milestone

### Task: Generate warehouses.csv with Missing Fields

**Your Role:** Data Engineer

**Instructions:**
1. Create `src/data_simulation/generate_warehouses.py`
2. Generate 20 warehouse records with:
   - warehouse_id, name, location (city)
   - latitude, longitude, capacity
   - manager_name, contact_phone, email
   - established_date, operating_hours

3. **Introduce Issues:**
   - 5% missing manager names
   - 10% missing contact phones
   - 3% missing emails
   - 2% duplicate warehouse entries

4. Output: `data/raw/warehouses.csv`
5. Commit and push

---

## Section 3: Instructions for Next AI Agent

### Milestone #8 Completed
- warehouses.csv (20), generate_warehouses.py
- 10% missing manager_name, 5% missing phone, 2 duplicates
- Next: Milestone #9