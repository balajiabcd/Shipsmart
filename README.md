# 🚚 Shipsmart: The Brain Behind Every Delivery

**"Shipsmart: The Brain Behind Every Delivery."**

---

## Project Overview

Shipsmart is an **end-to-end AI-powered logistics delay prediction system** designed to help logistics companies predict delivery delays before they occur. Built with maximum service provision using cutting-edge technologies including machine learning, LLMs, agent frameworks, and full-stack DevOps.

---

## Key Features

| Feature                       | Description                                       |
| ----------------------------- | ------------------------------------------------- |
| **Delay Prediction**    | Binary classification (delayed/on-time)           |
| **Duration Estimation** | Regression for delay minutes                      |
| **Root Cause Analysis** | SHAP + LLM explainability                         |
| **Decision Engine**     | Intelligent recommendations (reroute, reassign)   |
| **Chat Interface**      | LLM-powered natural language queries              |
| **Scenario Simulation** | What-if analysis for planning                     |
| **Anomaly Detection**   | Automated alerting for delay spikes               |
| **Route Optimization**  | Graph-based dynamic routing (Dijkstra + OR-Tools) |
| **Agent Framework**     | LangGraph + AutoGen + MCP integration             |

---

## Technology Stack

### Data Processing
- Pandas, NumPy, PyArrow
- Apache Spark (PySpark)

### Machine Learning
- **Classic ML**: scikit-learn, XGBoost, LightGBM, CatBoost
- **Deep Learning**: PyTorch, TensorFlow
- **Model Tracking**: MLflow

### LLM & AI
- **Local LLM**: Ollama (Llama 3, Mistral, Phi-3)
- **Cloud LLM**: OpenAI (GPT-4), Anthropic (Claude) - *requires API keys*
- **Agent Frameworks**: LangChain, LangGraph, AutoGen, MCP
- **Vector Databases**: ChromaDB, Pinecone, Weaviate, Qdrant, Milvus, FAISS

### API & Web
- **API**: FastAPI, Pydantic, Uvicorn
- **Frontend**: React, Next.js, TypeScript, Tailwind CSS
- **Dashboard**: Streamlit

### Database
- PostgreSQL, SQLite, Redis

### Infrastructure & Monitoring
- Docker, Kubernetes
- Helm
- Prometheus, Grafana, Loki

### CI/CD
- GitHub Actions

---

## Project Structure

```
Shipsmart/
├── project_planing/          # Planning documents
│   ├── plan/               # Original project plan
│   ├── milestones/          # Milestone tracking
│   ├── prompts/            # Milestone prompts
│   └── team/                # Team structure & chat logs
├── frontend/                # Next.js frontend application
├── src/                     # Source code
│   ├── data_simulation/    # Data generation scripts
│   ├── data_engineering/   # ETL pipelines
│   ├── ml_models/          # ML models (30+ classifiers/regressors)
│   ├── explainability/     # SHAP/LIME explanations
│   ├── decision_engine/    # Hybrid rule-based + ML engine
│   ├── llm/               # LLM integration (Ollama, routing)
│   ├── agents/            # Agent frameworks (LangGraph, AutoGen, MCP)
│   ├── rag/               # RAG pipeline implementations
│   ├── root_cause/        # Root cause analysis
│   ├── route_optimization/ # Dijkstra, A*, OR-Tools, TSP
│   ├── anomaly/           # Anomaly detection
│   ├── simulation/        # Scenario simulation
│   ├── features/          # Feature engineering
│   ├── external_apis/     # External API connectors
│   └── api/               # FastAPI application
│       ├── endpoints/     # API endpoints
│       └── dashboard/     # Streamlit dashboard
├── models/                 # Trained model artifacts
├── database/              # SQL schema & migrations
├── docker/                # Dockerfiles & compose
├── config/                # Kubernetes & Helm configs
├── observability/         # Prometheus, Grafana, Loki
├── tests/                 # Test suites
└── requirements.txt       # Python dependencies
```

---

## Getting Started

### Prerequisites

- Python 3.10+
- Docker & Docker Compose
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

# Generate simulated data
python src/data_simulation/generate_orders.py
python src/data_simulation/generate_drivers.py
# ... (run other generators as needed)

# Start services
cd docker
docker-compose up -d
```

---

## API Endpoints

| Endpoint                                   | Description                |
| ------------------------------------------ | -------------------------- |
| `POST /api/v1/predict`                   | Get delay prediction       |
| `POST /api/v1/predict/batch`             | Batch predictions          |
| `GET /api/v1/predict/model-info`         | Model information          |
| `GET /api/v1/predict/feature-importance` | Feature importance         |
| `POST /api/v1/recommend`                 | Get action recommendations |
| `POST /api/v1/explain`                   | Get delay explanations     |
| `POST /api/v1/chat`                      | Natural language queries   |
| `POST /api/v1/simulate`                  | Run scenario simulations   |
| `GET /api/v1/alerts`                     | Get active alerts          |
| `POST /api/v1/route/optimize`            | Get optimized routes       |
| `POST /api/v1/route/optimize/multi`      | Multi-route optimization   |

---

## Running the Application

### Development

```bash
# Start FastAPI server
python -m src.api.main

# API will be available at: http://localhost:8000
# API docs: http://localhost:8000/docs
```

### Streamlit Dashboard

```bash
# Install streamlit
pip install streamlit plotly requests

# Run dashboard
streamlit run src/api/dashboard/streamlit_dashboard.py

# Dashboard will open at: http://localhost:8501
```

### Docker Compose (All Services)

```bash
cd docker
docker-compose up -d

# Services:
# API:        http://localhost:8000
# Frontend:   http://localhost:3000
# Grafana:    http://localhost:3001 (admin/admin)
# Prometheus: http://localhost:9090
```

---

## Project Components

### Data Simulation (15+ generators)

- Orders, Drivers, Vehicles, Warehouses
- Routes, Locations, Weather, Traffic
- Holidays, Customers, Delivery Events

### ML Models (30+ models)

- Classification: Logistic Regression, Random Forest, XGBoost, LightGBM, CatBoost, SVM, Naive Bayes, KNN, Decision Tree, AdaBoost, Gradient Boosting, Extra Trees
- Regression: Linear, Ridge, Lasso, ElasticNet, Random Forest, XGBoost, LightGBM, CatBoost, SVR, KNN, Decision Tree, Extra Trees
- Neural Networks: PyTorch, TensorFlow (CNN, LSTM)

### AI Layer

- Decision Engine (hybrid rule-based + ML)
- LLM Integration (Ollama, OpenAI, Anthropic)
- RAG Pipeline (6+ vector databases)
- Agents (LangGraph, AutoGen, MCP)

### Explainability

- SHAP values, dependence, force, waterfall plots
- LIME explanations
- Permutation importance
- Partial dependence

---

## Documentation

- [Project Plan](./project_planing/plan/1_origin_plan.md)
- [Team Structure](./project_planing/team/team_structure.md)
- [Architecture](./docs/architecture.md)
- [API Reference](./docs/api.md)
- [Database Schema](./docs/database_schema.md)
- [Deployment Guide](./docs/guides/deployment.md)

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

| Role            | Responsibility                     |
| --------------- | ---------------------------------- |
| Team Lead       | Overall coordination, architecture |
| ML Engineer 1   | Classification models              |
| ML Engineer 2   | Regression, Neural Networks, SHAP  |
| Data Engineer   | ETL, Feature Engineering, APIs     |
| DevOps/MLOps    | K8s, CI/CD, Monitoring             |
| Full-Stack Dev  | FastAPI, React/Next.js             |
| AI/LLM Engineer | LLM, RAG, Agents                   |

---

*Project: Shipsmart - The Brain Behind Every Delivery*
*Tagline: "Shipsmart: The Brain Behind Every Delivery."*
