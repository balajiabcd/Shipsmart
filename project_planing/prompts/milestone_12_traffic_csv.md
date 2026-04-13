# Milestone #12: Generate Traffic CSV (Unclean)

---

## Section 1: Instructions from Previous AI Agent

*(To be filled by Milestone #11 agent)*

---

## Section 2: Detailed Prompt to Finish Milestone

### Task: Generate traffic.csv with Inconsistencies

**Your Role:** Data Engineer

**Instructions:**
1. Create `src/data_simulation/generate_traffic.py`
2. Generate 50,000 traffic records: date, route_id, hour, congestion_level (1-10), avg_speed
3. **Issues:** Inconsistent congestion_level values, 3% missing avg_speed
4. Output: `data/raw/traffic.csv`
5. Commit and push

---

## Section 3: Instructions for Next AI Agent

### Milestone #12 Completed
- traffic.csv (50K), generate_traffic.py
- 3% missing avg_speed, 2% inconsistent congestion
- Next: Milestone #13