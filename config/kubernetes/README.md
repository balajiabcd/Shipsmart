# Shipsmart Kubernetes Configuration

This directory contains Kubernetes manifests and Helm charts for deploying Shipsmart.

## Directory Structure

```
kubernetes/
├── namespace.yaml       # Namespace definitions
├── deployment.yaml      # API, ML, and Frontend deployments
├── service.yaml        # ClusterIP services
├── ingress.yaml        # Ingress rules
├── configmap.yaml      # Configuration values
├── secrets.yaml        # Sensitive data (update in production!)
├── pvc.yaml            # Persistent volume claims
├── hpa.yaml            # Horizontal pod autoscaling
├── pdb.yaml            # Pod disruption budgets
├── network-policy.yaml # Network policies
└── overlays/
    └── dev/
        └── kustomization.yaml  # Kustomize overlay

helm/shipsmart/
├── Chart.yaml
└── values.yaml
```

## Quick Start

### Using Kustomize (Recommended for dev)

```bash
# Apply all manifests
kubectl apply -k config/kubernetes/overlays/dev

# Check deployment status
kubectl get pods -n shipsmart
```

### Using Helm

```bash
# Install chart
helm install shipsmart ./config/helm/shipsmart

# Upgrade
helm upgrade shipsmart ./config/helm/shipsmart
```

## Components

- **API**: FastAPI service (port 8000)
- **ML Service**: Model inference service (port 8001)
- **Frontend**: Next.js dashboard (port 3000)
- **PostgreSQL**: Database (via Helm)
- **Redis**: Cache (via Helm)

## Scaling

- API: 2-10 replicas (HPA)
- ML: 1-5 replicas (HPA)
- Frontend: 1-5 replicas (HPA)

## Security

- Network policies restrict pod-to-pod communication
- Secrets should be updated with strong values in production
- TLS certificates managed by cert-manager 
