# Milestone #166: Document Decision Engine

**Your Role:** AI/LLM Engineer

Create decision engine documentation:

```markdown
# Shipsmart AI Decision Engine

## Architecture

The decision engine combines ML predictions with rule-based logic to provide actionable recommendations.

### Components

1. **Hybrid Engine** (`decision_engine/hybrid_engine.py`)
   - Combines ML predictions with business rules
   - Evaluates triggered rules based on delivery context
   - Generates ranked recommendations

2. **Rule System** (`decision_engine/rules.py`)
   - Predefined rules for reroute, driver reassignment, slot change
   - Condition evaluation logic
   - Priority-based rule execution

3. **Recommendation Modules**
   - `reroute.py` - Alternative route suggestions
   - `driver_assignment.py` - Driver reassignment logic
   - `slot_management.py` - Delivery slot recommendations
   - `notifications.py` - Proactive customer messaging

4. **Priority Queue** (`decision_engine/priority_queue.py`)
   - Handles multiple deliveries
   - Priority-based processing
   - Batch processing support

## API Endpoints

- POST /recommend/ - Get recommendations for a delivery
- GET /recommend/priority-queue - Get queued deliveries

## Decision Flow

1. Receive delivery context
2. Run ML model prediction
3. Evaluate triggered rules
4. Generate recommendations
5. Rank by impact score
6. Include cost-benefit analysis
7. Return prioritized actions

## Example Usage

```python
response = await client.post("/recommend/", json={
    "delivery_id": "DEL001",
    "origin": "Warehouse_A",
    "destination": "Customer_Location_1",
    "scheduled_time": "2024-01-15T10:00:00",
    "driver_id": "DRV001",
    "is_fragile": False,
    "customer_tier": "premium"
})
```

## Testing

See `tests/test_decision_engine.py` for comprehensive tests.
```

Save to `docs/decision_engine.md`. Commit.