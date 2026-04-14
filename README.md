# 🚚 Shipsmart: The Brain Behind Every Delivery

**"Shipsmart: The Brain Behind Every Delivery."**

---

## Project Overview

Shipsmart is an **end-to-end AI-powered logistics delay prediction system** designed to help logistics companies predict delivery delays before they occur. Built with maximum complexity using cutting-edge technologies including machine learning, LLMs, agent frameworks, and full-stack DevOps.

---

## Key Features

| Feature | Description |
|---------|-------------|
| **Delay Prediction** | Binary classification (delayed/on-time) |
| **Duration Estimation** | Regression for delay minutes |
| **Root Cause Analysis** | SHAP + LLM explainability |
| **Decision Engine** | Intelligent recommendations (reroute, reassign) |
| **Chat Interface** | LLM-powered natural language queries |
| **Scenario Simulation** | What-if analysis for planning |
| **Anomaly Detection** | Automated alerting for delay spikes |
| **Route Optimization** | Graph-based dynamic routing (Dijkstra + OR-Tools) |
| **Agent Framework** | LangGraph + AutoGen + MCP integration |

---

## Technology Stack

### Data Engineering
- Apache Spark, Pandas, Dask, Polars
- Apache Airflow, Prefect, Dagster
- PostgreSQL, Snowflake, Delta Lake

### Machine Learning
- XGBoost, LightGBM, CatBoost, scikit-learn
- PyTorch, TensorFlow (Neural Networks)
- MLflow, Weights & Biases, Feast

### LLM & AI
- Ollama (Llama 3, Mistral, Phi-3)
- OpenAI (GPT-4), Anthropic (Claude)
- LangChain, LangGraph, AutoGen
- ChromaDB, Pinecone, Weaviate, Qdrant, Milvus, FAISS

### API & Frontend
- FastAPI, Pydantic
- React, Next.js, TypeScript, Tailwind CSS

### Infrastructure
- Kubernetes (k3s/minikube), Docker
- Istio, Helm, ArgoCD
- Prometheus, Grafana, Loki, ELK Stack

### CI/CD
- GitHub Actions
- Terraform, Ansible

---

## Project Structure

```
Shipsmart/
├── project_planing/          # Planning documents
├── team_structure.md         # Team roles & workflow
├── communication_log.txt    # Team communication
├── data/                    # Data files
├── src/                     # Source code
│   ├── data_simulation/     # Data generation
│   ├── data_engineering/    # ETL pipelines
│   ├── ml_models/           # ML models
│   ├── explainability/      # SHAP/LIME
│   ├── ai_layer/            # AI components
│   ├── api/                 # FastAPI
│   └── frontend/            # React/Next.js
├── notebooks/               # Jupyter notebooks
├── models/                  # Trained models
├── config/                  # Configuration
├── docker/                  # Dockerfiles
├── ci/                      # CI/CD pipelines
└── observability/           # Monitoring
```

---

## Getting Started

### Prerequisites
- Python 3.10+
- Docker & Kubernetes
- GitHub account

### Installation

```bash
# Clone repository
git clone https://github.com/balajiabcd/Shipsmart
cd Shipsmart

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your API keys

# Run data simulation
python src/data_simulation/generate_all.py

# Start services
docker-compose up -d
```

---

## API Endpoints

| Endpoint | Description |
|----------|-------------|
| `/predict` | Get delay prediction |
| `/predict_proba` | Get probability scores |
| `/recommend` | Get action recommendations |
| `/explain` | Get delay explanations |
| `/chat` | Natural language queries |
| `/simulate` | Run scenario simulations |
| `/alerts` | Get active alerts |
| `/optimize_route` | Get optimized routes |

---

## Documentation

- [Project Plan](./project_planing/plan/1_origin_plan.md)
- [Team Structure](./team/team_structure.md)
- [User Guide](./docs/guides/user_guide.md)
- [API Reference](./docs/api/reference.md)
- [Architecture Diagram](./docs/architecture.md)
- [Deployment Guide](./docs/guides/deployment.md)
- [Operations Runbook](./docs/guides/runbook.md)

---

## Quick Start

### Development (Docker Compose)
```bash
# Start all services
cd docker
docker-compose up -d

# Services
# API:        http://localhost:8000
# Frontend:   http://localhost:3000
# Grafana:    http://localhost:3001 (admin/admin)
# Prometheus: http://localhost:9090
```

### Production (Kubernetes)
```bash
# Apply Kubernetes manifests
kubectl apply -k config/kubernetes/overlays/production

# Or install with Helm
helm install shipsmart config/helm/shipsmart
```

---

## Success Metrics

- Classification F1-Score: ≥ 0.90
- Classification ROC-AUC: ≥ 0.95
- Regression RMSE: ≤ 8 minutes
- API Response Time: < 300ms

---

## Version

**v1.0.0** - Initial Release (April 2026)

---

## Team

| Role | Responsibility |
|------|---------------|
| Team Lead | Overall coordination, architecture |
| ML Engineer 1 | Classification models |
| ML Engineer 2 | Regression, Neural Networks, SHAP |
| Data Engineer | ETL, Feature Engineering, APIs |
| DevOps/MLOps | K8s, CI/CD, Monitoring |
| Full-Stack Dev | FastAPI, React/Next.js |
| AI/LLM Engineer | LLM, RAG, Agents |

---

*Project: Shipsmart - The Brain Behind Every Delivery.*
*Tagline: "Shipsmart: The Brain Behind Every Delivery."*