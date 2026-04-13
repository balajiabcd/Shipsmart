# Milestone #333-355: ArgoCD, Scaling, Monitoring, Database

```yaml
# ArgoCD setup
# kubernetes/argocd.yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: shipsmart
  namespace: argocd
spec:
  project: default
  source:
    repoURL: https://github.com/balajiabcd/Shipsmart.git
    targetRevision: HEAD
    path: kubernetes/base
  destination:
    server: https://kubernetes.default.svc
    namespace: shipsmart
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
```

```yaml
# ML Model deployment - kubernetes/model-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: shipsmart-model
  namespace: shipsmart
spec:
  replicas: 2
  selector:
    matchLabels:
      app: shipsmart-model
  template:
    spec:
      containers:
      - name: model
        image: shipsmart/ml-model:latest
        ports:
        - containerPort: 8001
        resources:
          requests:
            memory: "2Gi"
            cpu: "1000m"
          limits:
            memory: "4Gi"
            cpu: "2000m"
        volumeMounts:
        - name: model-storage
          mountPath: /models
      volumes:
      - name: model-storage
        persistentVolumeClaim:
          claimName: model-pvc
---
# Horizontal Pod Autoscaler - kubernetes/hpa.yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: shipsmart-api-hpa
  namespace: shipsmart
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: shipsmart-api
  minReplicas: 2
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
---
# Pod Disruption Budget - kubernetes/pdb.yaml
apiVersion: policy/v1
kind: PodDisruptionBudget
metadata:
  name: shipsmart-api-pdb
  namespace: shipsmart
spec:
  minAvailable: 2
  selector:
    matchLabels:
      app: shipsmart-api
---
# Network Policy - kubernetes/network-policy.yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: shipsmart-network-policy
  namespace: shipsmart
spec:
  podSelector:
    matchLabels:
      app: shipsmart-api
  policyTypes:
  - Ingress
  - Egress
  ingress:
  - from:
    - namespaceSelector:
        matchLabels:
          name: shipsmart
  egress:
  - to:
    - namespaceSelector: {}
```

```yaml
# PostgreSQL - kubernetes/postgres.yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: postgres-pvc
  namespace: shipsmart
spec:
  accessModes:
  - ReadWriteOnce
  resources:
    requests:
      storage: 20Gi
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: postgres
  namespace: shipsmart
spec:
  containers:
  - name: postgres
    image: postgres:15
    env:
    - name: POSTGRES_DB
      value: shipsmart
    - name: POSTGRES_USER
      valueFrom:
        secretKeyRef:
          name: shipsmart-secrets
          key: postgres-user
    - name: POSTGRES_PASSWORD
      valueFrom:
        secretKeyRef:
          name: shipsmart-secrets
          key: postgres-password
    volumeMounts:
    - name: postgres-storage
      mountPath: /var/lib/postgresql/data
    resources:
      requests:
        memory: "512Mi"
        cpu: "250m"
```

```yaml
# Redis - kubernetes/redis.yaml
apiVersion: v1
kind: Service
metadata:
  name: redis
  namespace: shipsmart
spec:
  ports:
  - port: 6379
  selector:
    app: redis
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: redis
  namespace: shipsmart
spec:
  replicas: 1
  selector:
    matchLabels:
      app: redis
  template:
    spec:
      containers:
      - name: redis
        image: redis:7-alpine
        ports:
        - containerPort: 6379
        resources:
          limits:
            memory: "256Mi"
```

Commit all deployment configs.