# 🗄️ Database Strategy (SQLite vs PostgreSQL)

## 🎯 Core Rule

```
DEV (simple) → SQLite
DEV (realistic) → PostgreSQL (Docker)
PROD → PostgreSQL ONLY
```

<br>


## 📊 Database Mapping by Mode

| Mode              | Environment | Database   | Why                            |
| ----------------- | ----------- | ---------- | ------------------------------ |
| Local (no Docker) | DEV         | SQLite     | Zero setup, fastest start      |
| Docker (local)    | DEV         | PostgreSQL | Mirrors production             |
| Docker → ECR      | PROD        | PostgreSQL | Container standard             |
| AWS App Runner    | PROD        | PostgreSQL | Required for scaling           |
| Kubernetes        | DEV/PROD    | PostgreSQL | Distributed system requirement |


<br>


## 🧠 Decision Logic

### SQLite

Used in:
- Local development (no Docker)

Why:
- No installation
- File-based (`db.sqlite3`)
- Instant startup

Limitations:
- No concurrency
- Not production-safe
- No scaling

### PostgreSQL

Used in:
- Docker (local dev)
- AWS (App Runner)
- Kubernetes

Why:
- Production-grade
- Handles concurrency
- Network-accessible
- Same behavior across environments

<br>

## 🔗 Environment → Database Mapping

| Environment | Execution Mode        | Database   |
| ----------- | --------------------- | ---------- |
| DEV         | Local Python          | SQLite     |
| DEV         | Docker                | PostgreSQL |
| DEV         | Kubernetes (optional) | PostgreSQL |
| PROD        | App Runner            | PostgreSQL |
| PROD        | Kubernetes            | PostgreSQL |

<br>

## 🐳 Docker Setup (PostgreSQL)

Defined in:

```
docker-compose.yml
```

Includes:
- `db` service (Postgres)
- Django connected via `DATABASE_URL`

<br>

## ⚙️ Environment Variables

### SQLite (Local)

```
DB_ENGINE=sqlite
DB_NAME=db.sqlite3
```

### PostgreSQL (Docker / PROD)

```
DB_ENGINE=postgres
DB_NAME=app_db
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=db
DB_PORT=5432
```

<br>

## 🔄 Switching Logic

```
if DB_ENGINE == "sqlite":
    # use SQLite
else:
    # use PostgreSQL
```

<br>

## 🚨 Common Pitfall

Developing only on SQLite → issues in production

Recommended:

```
Start with SQLite → switch to Docker Postgres early
```

<br>

## 🧭 Recommended DB Workflow

### Early Development
```
SQLite (fast iteration)
```

### Feature Development
```
Docker + PostgreSQL (real environment)
```

### Production
```
PostgreSQL only (ECR → App Runner / K8s)
```

<br>

## 🧱 DB Architecture View

```
[LOCAL SIMPLE]
  └── SQLite (file)

[LOCAL DOCKER]
  └── PostgreSQL (container)

[AWS / PROD]
  └── PostgreSQL (managed / container)

[KUBERNETES]
  └── PostgreSQL (stateful service)
```


<br>

## ✅ TL;DR

- SQLite = speed
- PostgreSQL = reality
- PROD = PostgreSQL only
- Always test on Postgres before deploying
