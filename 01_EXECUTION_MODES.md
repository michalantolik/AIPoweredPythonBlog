# 🚀 Execution modes

This application supports multiple execution modes:

- Local Standard
- Local Docker
- Local Kubernetes
- Cloud AWS (ECR + App Runner)
- Cloud AWS Kubernetes
  
<br>


# 🌍 Environments overview

| Environment | Purpose               | Where it runs                      | Typical usage      |
| ----------- | --------------------- | ---------------------------------- | ------------------ |
| **DEV**     | Development & testing | Local / Docker / K8s (dev cluster) | Developer workflow |
| **PROD**    | Production            | AWS (App Runner / K8s)             | Live system        |

<br>


# 🔗 Environments mapping

| Mode              | DEV           | PROD                    |
| ----------------- | ------------  | ----------------------- |
| Local Standard    | ✅ Primary    | ❌ Never               |
| Local Docker      | ✅ Primary    | ⚠️ Only for testing    |
| Docker → ECR      | ❌            | ✅ Required            |
| AWS App Runner    | ❌            | ✅ Primary             |
| Kubernetes        | ✅ (optional) | ✅ Advanced production |

<br>


# 🧠 Core principle

- **DEV = fast iteration**
- **PROD = containerized, reproducible, cloud-ready**

<br>


# 🖥️ 1. Local Standard

✅ **DEV ONLY**

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

# 🐳 2. Local Docker

✅ **DEV (recommended)**
⚠️ **Can simulate PROD**

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
