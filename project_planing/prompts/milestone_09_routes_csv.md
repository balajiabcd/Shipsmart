# Milestone #9: Generate Routes CSV (Unclean)

---

## Section 1: Instructions from Previous AI Agent

*(To be filled by Milestone #8 agent)*

---

## Section 2: Detailed Prompt to Finish Milestone

### Task: Generate routes.csv with Duplicates

**Your Role:** Data Engineer

**Instructions:**
1. Create `src/data_simulation/generate_routes.py`
2. Generate 1,000 route records with:
   - route_id, origin_city, destination_city
   - distance_km, avg_duration_minutes
   - route_type (highway, secondary, local)
   - traffic_level (low, medium, high)

3. **Introduce Issues:**
   - 3% duplicate routes (same origin/dest, different IDs)
   - 2% inconsistent route types
   - 5% missing avg_duration

4. Output: `data/raw/routes.csv`
5. Commit and push

---

## Section 3: Instructions for Next AI Agent

### Milestone #9 Completed
- routes.csv (1000), generate_routes.py
- 5% missing avg_duration, 15 duplicates, 2% unknown type
- Next: Milestone #10