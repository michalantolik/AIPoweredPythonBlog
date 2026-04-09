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

Flow:
- Push image to ECR
- App Runner pulls image
- App runs as managed service

📌 Pros:
- No infra management
- Auto scaling
- HTTPS out of the box
