# Milestone #312-332: Kubernetes & MLOps Infrastructure

```bash
# Phase 17 - Kubernetes Setup
# Install minikube or k3s
minikube start --cpus=4 --memory=8192
kubectl config use-context minikube
```

```yaml
# kubernetes/namespace.yaml
apiVersion: v1
kind: Namespace
metadata:
  name: shipsmart
---
# kubernetes/deployment-api.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: shipsmart-api
  namespace: shipsmart
spec:
  replicas: 3
  selector:
    matchLabels:
      app: shipsmart-api
  template:
    metadata:
      labels:
        app: shipsmart-api
    spec:
      containers:
      - name: api
        image: shipsmart/api:latest
        ports:
        - containerPort: 8000
        resources:
          requests:
            memory: "512Mi"
            cpu: "250m"
          limits:
            memory: "1Gi"
            cpu: "500m"
        env:
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: shipsmart-secrets
              key: database-url
---
# kubernetes/service-api.yaml
apiVersion: v1
kind: Service
metadata:
  name: shipsmart-api
  namespace: shipsmart
spec:
  selector:
    app: shipsmart-api
  ports:
  - port: 80
    targetPort: 8000
---
# kubernetes/ingress.yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: shipsmart-ingress
  namespace: shipsmart
  annotations:
    nginx.ingress.kubernetes.io/rewrite-target: /
spec:
  rules:
  - host: shipsmart.local
    http:
      paths:
      - path: /api
        pathType: Prefix
        backend:
          service:
            name: shipsmart-api
            port:
              number: 80
---
# kubernetes/configmap.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: shipsmart-config
  namespace: shipsmart
data:
  LOG_LEVEL: "INFO"
  REDIS_HOST: "redis"
---
# kubernetes/secrets.yaml
apiVersion: v1
kind: Secret
metadata:
  name: shipsmart-secrets
  namespace: shipsmart
type: Opaque
stringData:
  database-url: "postgresql://user:pass@postgres:5432/shipsmart"
  api-key: "your-api-key-here"
```

```bash
# Helm chart setup
helm create shipsmart
# Customize values.yaml for different environments
kubectl apply -k kubernetes/overlays/dev
```

Commit Kubernetes manifests.