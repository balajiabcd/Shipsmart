# Milestone #19: Generate Vehicle Maintenance CSV

---

## Section 1: Instructions from Previous AI Agent

*(To be filled by Milestone #18 agent)*

---

## Section 2: Detailed Prompt to Finish Milestone

### Task: Generate vehicle_maintenance.csv

**Your Role:** Data Engineer

**Instructions:**
1. Create `src/data_simulation/generate_vehicle_maintenance.py`
2. Generate 5,000 maintenance records: vehicle_id, date, maintenance_type, cost, description, next_due_date
3. **Issues:** Random gaps in records, 5% missing next_due_date
4. Output: `data/raw/vehicle_maintenance.csv`
5. Commit and push

---

## Section 3: Instructions for Next AI Agent

### Milestone #19 Completed
- vehicle_maintenance.csv (5K), generate_vehicle_maintenance.py
- 5% missing next_maintenance_due, 3% gaps
- Next: Milestone #20