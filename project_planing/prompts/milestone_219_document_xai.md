# Milestone #219: Document Root Cause System

**Your Role:** AI/LLM Engineer

Write XAI documentation:

```markdown
# Shipsmart Explainable AI (XAI) System

## Overview

Root cause analysis combining SHAP values with LLM-generated natural language explanations.

## Components

### 1. SHAP + LLM Integration (`src/root_cause/shap_llm_integration.py`)
- Computes SHAP values for each prediction
- Identifies top contributing features
- Generates NL explanations via LLM

### 2. Prompt Templates (`src/root_cause/prompts.py`)
- Delay prediction prompts
- Driver analysis prompts
- Weather impact prompts
- Route analysis prompts

### 3. NL Generator (`src/root_cause/generator.py`)
- Human-readable explanations
- Batch processing support
- Markdown formatting

### 4. Confidence Scoring (`src/root_cause/confidence.py`)
- Prediction confidence
- SHAP quality confidence
- Data quality confidence
- Overall rating

### 5. Visualizations (`src/root_cause/visualizations.py`)
- Waterfall charts
- Factor importance plots
- Confidence gauges

## API Endpoints

- POST /explain/ - Get full explanation
- GET /explain/root-causes/{id} - Get root causes only

## Example

```json
{
  "delivery_id": "DEL001",
  "prediction": 0.78,
  "explanation": "Heavy rain and high traffic are the main factors...",
  "root_causes": ["weather_severity", "traffic_index"],
  "confidence": "high"
}
```

Save to `docs/root_cause_system.md`. Commit.