# Milestone #6: Generate Drivers CSV (Unclean)

---

## Section 1: Instructions from Previous AI Agent

**From Milestone #5:**
- orders.csv generated with 100K records

---

## Section 2: Detailed Prompt to Finish Milestone

### Task: Generate drivers.csv with Inconsistencies

**Project Context:**
- Project: Shipsmart
- **GitHub Repository:** https://github.com/balajiabcd/Shipsmart

**Your Role:**
You are a **Data Engineer** generating synthetic driver data.

**Instructions:**

1. **Create Python Script**
   Create `src/data_simulation/generate_drivers.py`:

   Generate 500 driver records with:
   - driver_id, name, license_number
   - hire_date (inconsistent date formats: DD/MM/YYYY, YYYY-MM-DD, MM-DD-YYYY)
   - license_expiry
   - vehicle_id assigned
   - status (active, on_leave, suspended)
   - rating (1-5 stars)
   - total_deliveries

2. **Introduce Data Quality Issues:**
   - 5% inconsistent date formats
   - 2% missing license numbers
   - 3% duplicate entries (same driver with different IDs)
   - 1% invalid phone numbers

3. **Run and Save**
   ```bash
   python src/data_simulation/generate_drivers.py
   # Output: data/raw/drivers.csv
   ```

4. **Commit and Push**

**Subagent Task:** None needed for this milestone.

---

## Section 3: Instructions for Next AI Agent

### Milestone #6 Completed

**Created:**
- `data/raw/drivers.csv` - 500 drivers
- `src/data_simulation/generate_drivers.py`

**Data Quality Issues:**
- ~5% inconsistent date formats (DD/MM/YYYY, MM-DD-YYYY, YYYY-MM-DD)
- ~2.6% missing license_number
- ~12% missing vehicle_id
- 15 duplicate driver names
- 1% invalid phone numbers

**Status:** active (434), on_leave (38), suspended (28)

**Next:** Milestone #7 - Vehicles CSV ✅ COMPLETED