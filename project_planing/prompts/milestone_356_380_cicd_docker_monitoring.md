# Milestone #356-380: CI/CD Pipeline, Docker, Monitoring

```yaml
# .github/workflows/ci.yml
name: CI/CD Pipeline
on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v4
    - uses: actions/setup-python@v5
      with:
        python-version: '3.11'
    - run: pip install -r requirements.txt
    - run: pytest tests/ --cov
    - run: ruff check .

  build:
    needs: test
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v4
    - uses: docker/setup-buildx-action@v3
    - uses: actions/cache@v4
      with:
        path: /tmp/.buildx-cache
        key: ${{ runner.os }}-buildx-${{ github.sha }}
    - run: docker build -t shipsmart/api:${{ github.sha }} ./api
    - run: docker build -t shipsmart/ml-model:${{ github.sha }} ./ml
    - run: docker build -t shipsmart/frontend:${{ github.sha }} ./frontend

  deploy:
    needs: build
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v4
    - run: kubectl set image deployment/shipsmart-api api=shipsmart/api:${{ github.sha }}
```

```dockerfile
# Dockerfile.api
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0"]

# Dockerfile.ml
FROM python:3.11-slim
WORKDIR /app
COPY models/ ./models
RUN pip install scikit-learn xgboost shap
EXPOSE 8001
CMD ["python", "serve_model.py"]

# Dockerfile.frontend
FROM node:20-alpine as builder
WORKDIR /app
COPY frontend/package*.json .
RUN npm ci
COPY frontend/ .
RUN npm run build
FROM nginx:alpine
COPY --from=builder /app/.next /usr/share/nginx/html
EXPOSE 80
```

```yaml
# docker-compose.yml
version: '3.8'
services:
  api:
    build: ./api
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://user:pass@postgres:5432/shipsmart
      - REDIS_HOST=redis
    depends_on:
      - postgres
      - redis

  ml-model:
    build: ./ml
    ports:
      - "8001:8001"

  frontend:
    build: ./frontend
    ports:
      - "3000:80"

  postgres:
    image: postgres:15
    environment:
      POSTGRES_DB: shipsmart
      POSTGRES_USER: user
      POSTGRES_PASSWORD: pass
    volumes:
      - postgres_data:/var/lib/postgresql/data

  redis:
    image: redis:7-alpine

volumes:
  postgres_data:
```

```yaml
# Prometheus monitoring - kubernetes/prometheus.yaml
apiVersion: monitoring.coreos.com/v1
kind: ServiceMonitor
metadata:
  name: shipsmart-monitor
  namespace: shipsmart
spec:
  selector:
    matchLabels:
      app: shipsmart-api
  endpoints:
  - port: metrics

# Grafana dashboard
apiVersion: v1
kind: ConfigMap
metadata:
  name: grafana-dashboard
  namespace: monitoring
data:
  dashboard.json: |
    { "panels": [...] }
```

Commit CI/CD and monitoring configs.