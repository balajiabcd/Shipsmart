# Milestone #11: Generate Weather CSV (Unclean)

---

## Section 1: Instructions from Previous AI Agent

*(To be filled by Milestone #10 agent)*

---

## Section 2: Detailed Prompt to Finish Milestone

### Task: Generate weather.csv with Null Values

**Your Role:** Data Engineer

**Instructions:**
1. Create `src/data_simulation/generate_weather.py`
2. Generate 50,000 weather records:
   - date, location_id
   - temperature (°C), condition (rain/snow/clear/cloudy/fog)
   - humidity (%), wind_speed (km/h)
3. **Introduce Issues:**
   - 10% null values in temperature
   - 8% null values in humidity
   - 5% null values in wind_speed
4. Output: `data/raw/weather.csv`
5. Commit and push

**Subagent Task:** None needed for this milestone.

---

## Section 3: Instructions for Next AI Agent

### Milestone #11 Completed
- weather.csv (50K), generate_weather.py
- 10% missing temp, 8% humidity, 5% wind_speed
- Next: Milestone #12