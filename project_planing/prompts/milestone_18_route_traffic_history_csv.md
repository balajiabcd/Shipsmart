# Milestone #18: Generate Route Traffic History CSV

---

## Section 1: Instructions from Previous AI Agent

*(To be filled by Milestone #17 agent)*

---

## Section 2: Detailed Prompt to Finish Milestone

### Task: Generate route_traffic_history.csv

**Your Role:** Data Engineer

**Instructions:**
1. Create `src/data_simulation/generate_route_traffic_history.py`
2. Generate 100,000 historical traffic records: route_id, date, hour, traffic_level (low/medium/high), avg_speed, incidents
3. **Issues:** Inconsistent traffic_level values, 2% missing avg_speed
4. Output: `data/raw/route_traffic_history.csv`
5. Commit and push

---

## Section 3: Instructions for Next AI Agent

### Milestone #18 Completed
- route_traffic_history.csv (100K), generate_route_traffic_history.py
- 2% missing speed, 2% unknown traffic level
- Next: Milestone #19