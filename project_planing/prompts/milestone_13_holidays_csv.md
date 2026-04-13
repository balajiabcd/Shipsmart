# Milestone #13: Generate Holidays CSV (Unclean)

---

## Section 1: Instructions from Previous AI Agent

*(To be filled by Milestone #12 agent)*

---

## Section 2: Detailed Prompt to Finish Milestone

### Task: Generate holidays.csv with Format Issues

**Your Role:** Data Engineer

**Instructions:**
1. Create `src/data_simulation/generate_holidays.py`
2. Generate 500 holiday records: date, country, region, holiday_name, type (public/bank/movable)
3. **Issues:** Inconsistent date formats (DD/MM/YYYY, YYYY-MM-DD, MM/DD/YYYY), 5% missing regions
4. Output: `data/raw/holidays.csv`
5. Commit and push

---

## Section 3: Instructions for Next AI Agent

### Milestone #13 Completed
- holidays.csv (500), generate_holidays.py
- 5% missing region, 6% inconsistent dates, 10 duplicates
- Next: Milestone #14