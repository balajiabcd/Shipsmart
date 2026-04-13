# Milestone #7: Generate Vehicles CSV (Unclean)

---

## Section 1: Instructions from Previous AI Agent

**From Milestone #6:**
- drivers.csv generated with 500 records

---

## Section 2: Detailed Prompt to Finish Milestone

### Task: Generate vehicles.csv with Outliers

**Project Context:**
- Project: Shipsmart

**Your Role:**
You are a **Data Engineer** generating vehicle data.

**Instructions:**

1. Create `src/data_simulation/generate_vehicles.py`
2. Generate 300 vehicle records with:
   - vehicle_id, type (van, truck, motorcycle), capacity_kg
   - plate_number, manufacturing_year
   - maintenance_due_date, insurance_expiry
   - status (active, maintenance, retired)

3. **Introduce Issues:**
   - 2% outliers in capacity (some values 10x normal)
   - 5% missing maintenance dates
   - 1% duplicate plates

4. Run and save to `data/raw/vehicles.csv`
5. Commit and push

---

## Section 3: Instructions for Next AI Agent

### Milestone #7 Completed

**Created:**
- `data/raw/vehicles.csv` - 300 vehicles
- `src/data_simulation/generate_vehicles.py`

**Data Quality Issues:**
- ~1% outlier capacity (10x)
- ~6% missing maintenance_due
- 3 duplicate plates

**Status:** active (256), maintenance (29), retired (15)

**Next:** Milestone #8 - Warehouses CSV