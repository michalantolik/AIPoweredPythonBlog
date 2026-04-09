## 🚀 Execution modes

This application supports multiple execution modes:

- Local Standard
- Local Docker
- Local Kubernetes
- Cloud AWS (ECR + App Runner)
- Cloud AWS Kubernetes
  
<br>


## 🌍 Environments overview

| Environment | Purpose               | Where it runs                      | Typical usage      |
| ----------- | --------------------- | ---------------------------------- | ------------------ |
| **DEV**     | Development & testing | Local / Docker / K8s (dev cluster) | Developer workflow |
| **PROD**    | Production            | AWS (App Runner / K8s)             | Live system        |

<br>


## 🔗 Environments mapping

| Mode              | DEV           | PROD                    |
| ----------------- | ------------  | ----------------------- |
| Local Standard    | ✅ Primary    | ❌ Never               |
| Local Docker      | ✅ Primary    | ⚠️ Only for testing    |
| Docker → ECR      | ❌            | ✅ Required            |
| AWS App Runner    | ❌            | ✅ Primary             |
| Kubernetes        | ✅ (optional) | ✅ Advanced production |

<br>


## 🧠 Core principle

- **DEV = fast iteration**
- **PROD = containerized, reproducible, cloud-ready**

<br>


## 🖥️ 1. Local Standard

### ✅ DEV ONLY

Runs Django directly.

```bash
cd AIPoweredPythonBlog

pip install -r requirements.txt
cp .env.example .env

python manage.py migrate
```

📌 Notes:
- Fastest feedback loop
- Uses `.env`
- No container isolation

<br>


## 🐳 2. Local Docker

### ✅ DEV (recommended)
### ⚠️ Can simulate PROD

```bash
docker-compose up --build
```

📌 Uses:
- `Dockerfile`
- `docker-compose.yml`
- `.env.docker`

📌 Benefits:
- Same runtime as production
- Includes DB (Postgres)

<br>


## 📦 3. Docker Image (Build Once)

This is the **bridge between DEV and PROD**

```bash
docker build -t ai-blog .
```

<br>

## ☁️ 4. Push to Amazon ECR

### ✅ REQUIRED FOR PROD

GitHub Action:
```bash
.github/workflows/ecr.yml
```

Manual flow:
```bash
aws ecr get-login-password ...

docker tag ai-blog:latest <ECR_URL>
docker push <ECR_URL>
```

📌 Output:
- Versioned container image in AWS

<br>


## 🚀 5. AWS App Runner (PROD)

### ✅ PRIMARY PRODUCTION MODE

Uses:
```bash
.github/workflows/deploy-app-runner.yml
terraform/apprunner.tf
```

📌 Flow:
- Push image to ECR
- App Runner pulls image
- App runs as managed service

📌 Pros:
- No infra management
- Auto scaling
- HTTPS out of the box

<br>


## ☸️ 6. Kubernetes Deployment

### ✅ ADVANCED (DEV or PROD)

Configs:
```bash
k8s/
  django.yaml
  postgres.yaml
  configmap.yaml
  secret.yaml
```

Deploy:
```bash
kubectl apply -f k8s/
```

📌 Use cases:
- Full control
- Microservices architecture
- Enterprise setups

<br>


## ⚙️ 7. CI/CD (GitHub Actions)

### Pipelines:

| Workflow                | Purpose                   |
| ----------------------- | ------------------------- |
| `ci.yml`                | Tests / validation        |
| `ecr.yml`               | Build & push Docker image |
| `deploy-app-runner.yml` | Deploy to AWS             |

<br>


## 🔄 Full Deployment Flow (PROD)

```bash
Code → GitHub → CI → Build Docker → Push to ECR → Deploy → App Runner
```

<br>


## 🧩 Environment Variables

| File          | Used in           |
| ------------- | ----------------- |
| `.env`        | Local (no Docker) |
| `.env.docker` | Docker            |
| AWS Secrets   | App Runner / PROD |
| K8s Secrets   | Kubernetes        |

<br>


## ⚠️ Key Differences: DEV vs PROD

| Aspect    | DEV                    | PROD                      |
| --------- | ---------------------- | ------------------------- |
| Debug     | ON                     | OFF                       |
| DB        | Standard / Docker      | Managed (RDS / container) |
| Secrets   | `.env` / `.env.docker` | AWS / K8s secrets         |
| Scaling   | None                   | Auto                      |
| Stability | Low                    | High                      |

<br>


## 🧭 Recommended Workflow

### Daily Development
```bash
Local → Docker → Commit → Push
```

### Production Deployment
```bash
Push → CI → ECR → App Runner
```

<br>


## 🧱 Architecture Summary

[LOCAL DEV]
  └── Python / Docker

[BUILD]
  └── Docker Image

[REGISTRY]
  └── Amazon ECR

[DEPLOY]
  ├── App Runner (default)
  └── Kubernetes (advanced)

<br>


## ✅ TL;DR
- Use **local Python** for quick dev
- Use **Docker** for consistency
- Use **ECR + App Runner** for production
- Use **Kubernetes** only if needed
