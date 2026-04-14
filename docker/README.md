# CI/CD Pipeline, Docker & Monitoring

This directory contains the CI/CD configuration, Docker files, and monitoring setup for Shipsmart.

## Structure

```
.
├── .github/
│   └── workflows/
│       └── ci.yml                 # GitHub Actions CI/CD pipeline
├── docker/
│   ├── api/
│   │   └── Dockerfile             # FastAPI service container
│   ├── ml/
│   │   └── Dockerfile             # ML model service container
│   ├── frontend/
│   │   ├── Dockerfile             # Next.js frontend container
│   │   └── nginx.conf             # Nginx configuration
│   └── compose.yml                # Full stack docker-compose
└── config/
    └── kubernetes/
        └── service-monitor.yaml   # Prometheus ServiceMonitors
```

## GitHub Actions Pipeline (Milestones 356-376)

### Jobs:
1. **lint** - Code quality with Ruff
2. **test** - Run pytest with coverage
3. **security** - Trivy vulnerability scan + Bandit
4. **build** - Docker build for API, ML, Frontend (on push only)
5. **deploy-staging** - Deploy to staging (develop branch)
6. **deploy-production** - Deploy to production (main branch)

### Pipeline Flow:
```
push to develop → lint + test + security → build → deploy-staging
push to main    → lint + test + security → build → deploy-production
```

## Docker Images

### API (Milestone 363)
- Python 3.11-slim base
- FastAPI application
- Health checks enabled

### ML Service
- Python 3.11-slim base
- scikit-learn, xgboost, lightgbm
- Model serving on port 8001

### Frontend (Milestone 363)
- Node 20 Alpine for build
- Nginx Alpine for serving
- Next.js static output

## Docker Compose

Run full stack locally:
```bash
cd docker
docker-compose up -d
```

Services:
- `api` - http://localhost:8000
- `ml-service` - http://localhost:8001
- `frontend` - http://localhost:3000
- `postgres` - localhost:5432
- `redis` - localhost:6379
- `prometheus` - http://localhost:9090
- `grafana` - http://localhost:3001 (admin/admin)

## Kubernetes Deployment (Milestones 364-376)

ServiceMonitors for Prometheus scraping in K8s:
```bash
kubectl apply -f config/kubernetes/service-monitor.yaml
```

## Security Scanning

- **Trivy** - Container vulnerability scanning
- **Bandit** - Python security analysis
- **CodeQL** - GitHub native SAST

## Environment Promotion

```
develop → staging → production
```

Each environment has its own Kubernetes context and image tags. 
