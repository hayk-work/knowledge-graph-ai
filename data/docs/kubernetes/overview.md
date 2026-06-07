# Kubernetes (K8s) Overview

Kubernetes is an open-source container orchestration platform. It automates deploying,
scaling, and operating application containers across clusters of machines.

## Core Concepts

### Cluster

A cluster has a control plane (API server, scheduler, controller manager) and worker nodes
that run your workloads.

### Pod

The smallest deployable unit. A pod wraps one or more containers that share network and
storage. Most apps run one main container per pod.

### Deployment

A Deployment manages replicated pods from a pod template. You declare desired replicas and
image version; Kubernetes reconciles actual state toward desired state.

### Service

Pods are ephemeral—their IPs change. A Service provides a stable network endpoint and load
balances traffic to matching pods. Types include ClusterIP, NodePort, and LoadBalancer.

### Namespace

Namespaces isolate resources within a cluster (e.g. `dev`, `staging`, `production`).

## Declarative Configuration

You describe desired state in YAML manifests:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: api
spec:
  replicas: 3
  template:
    spec:
      containers:
        - name: api
          image: myapp:1.0.0
          ports:
            - containerPort: 8000
```

Apply with `kubectl apply -f deployment.yaml`.

## Scaling and Health

Kubernetes supports horizontal pod autoscaling based on CPU or custom metrics. Liveness and
readiness probes restart unhealthy containers and remove not-ready pods from service traffic.

## ConfigMaps and Secrets

Inject configuration and sensitive values without baking them into images. Mount as files or
environment variables.

## Ingress

Ingress controllers route external HTTP(S) traffic to services inside the cluster, often
with TLS termination and path-based routing.

## Common kubectl Commands

- `kubectl get pods` — list pods
- `kubectl logs <pod>` — view container logs
- `kubectl describe deployment <name>` — inspect events and status
- `kubectl port-forward svc/api 8000:80` — local access to a service

## K8s and AI Workloads

ML and RAG services often run as Deployments behind Services, with GPU node pools for
inference and separate jobs for batch embedding or indexing pipelines.
