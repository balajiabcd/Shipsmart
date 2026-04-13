# Milestone #231: Document Simulation System

**Your Role:** AI/LLM Engineer

Write simulation documentation:

```markdown
# Shipsmart Simulation System

## Overview

Scenario simulation framework for testing delivery operations under various conditions.

## Scenarios

| Scenario | Description | Parameters |
|----------|-------------|------------|
| Demand Increase | Test with increased order volume | multiplier: 1.0-3.0 |
| Driver Shortage | Test with fewer available drivers | shortage: 0-100% |
| Weather Impact | Test various weather conditions | scenario: clear/rain/storm/snow/fog |
| Fuel Price | Test fuel cost variations | change: -50% to +50% |
| Warehouse Outage | Test facility failure | warehouse_id |
| Competitor | Test market dynamics | price_change |

## Architecture

1. **SimulationFramework** (`src/simulation/framework.py`)
   - Base class for all simulations
   - State management
   - History tracking

2. **Scenario Builder** (`src/simulation/scenario_builder.py`)
   - Parameter configuration
   - Scenario composition

3. **Visualizations** (`src/simulation/visualization.py`)
   - Timeline plots
   - Scenario comparisons

## API Endpoints

- POST /simulate/ - Run simulation
- GET /simulate/scenarios - List available scenarios

## Example

```bash
curl -X POST http://localhost:8000/simulate/ \
  -H "Content-Type: application/json" \
  -d '{
    "scenario_type": "weather",
    "parameters": {"weather": "storm", "duration": 24}
  }'
```

Save to `docs/simulation_system.md`. Commit.