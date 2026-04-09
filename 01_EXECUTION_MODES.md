# 🚀 Execution modes

This application supports multiple execution modes:

- Local (standard)
- Local (docker)
- AWS (ECR + App Runner)
- Kubernetes (k8s manifests)

# 🌍 Environments overview

| Environment | Purpose               | Where it runs                      | Typical usage      |
| ----------- | --------------------- | ---------------------------------- | ------------------ |
| **DEV**     | Development & testing | Local / Docker / K8s (dev cluster) | Developer workflow |
| **PROD**    | Production            | AWS (App Runner / K8s)             | Live system        |
