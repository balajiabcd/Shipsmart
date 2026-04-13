# Milestone #15: Generate Delivery Events CSV

---

## Section 1: Instructions from Previous AI Agent

*(To be filled by Milestone #14 agent)*

---

## Section 2: Detailed Prompt to Finish Milestone

### Task: Generate delivery_events.csv

**Your Role:** Data Engineer

**Instructions:**
1. Create `src/data_simulation/generate_delivery_events.py`
2. Generate 200,000 event records: event_id, order_id, timestamp, event_type (created/picked_up/in_transit/out_for_delivery/delivered/failed), location_id
3. **Issues:** 3% missing timestamps, 1% missing locations
4. Output: `data/raw/delivery_events.csv`
5. Commit and push

---

## Section 3: Instructions for Next AI Agent

### Milestone #15 Completed
- delivery_events.csv (200K), generate_delivery_events.py
- 3% missing timestamps, 1% missing location_id
- Next: Milestone #16