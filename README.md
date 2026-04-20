# 🚀 Two-Tier Application (Flask + MySQL) build

![Docker](https://img.shields.io/badge/Docker-Automated-2496ED?logo=docker)
![CI/CD](https://img.shields.io/badge/CI%2FCD-GitHub_Actions-2088FF?logo=githubactions)
![Auth](https://img.shields.io/badge/Auth-Flask--Bcrypt-orange)
![Security](https://img.shields.io/badge/Security-DevSecOps-red)

A hands-on two-tier web application built with Flask (backend) and MySQL (database), with a full **DevSecOps pipeline** using GitHub Actions. Built from scratch for learning Docker, CI/CD, and production-grade security practices.

> 🎯 **Goal:** Learn Docker & DevSecOps by *building everything yourself* instead of just running ready-made configs.

---

## 🧩 Application Overview

A **Todo List application** with full user authentication where:

- Users can register and log in to their own account
- Each user manages only their own tasks
- Tasks can be added, completed, renamed, and soft-deleted
- All auth activity is tracked in the database (login / logout / failed attempts with IP + timestamp)
- All data stored persistently in MySQL

---

## 🗂️ Project Structure

```
two-tier-app/
├── app.py                        # Flask application logic
├── requirements.txt              # Python dependencies
├── schema.sql                    # MySQL schema (users, todos, auth_logs)
├── dockerfile                    # Single-stage Dockerfile
├── docker-compose.yml            # Orchestration config
├── templates/
│   ├── index.html                # Main todo UI
│   ├── login.html                # Login page
│   ├── register.html             # Registration page
│   └── deleted.html              # Deleted todos view
├── .github/
│   └── workflows/
│       ├── DevSecOps-pipeline.yml    # Main orchestrator pipeline
│       ├── code-quality.yml          # flake8 + bandit
│       ├── dependencies-scan.yml     # pip-audit
│       ├── secrets-scan.yml          # gitleaks
│       ├── dockerfile-scan.yml       # hadolint
│       ├── docker-build-push.yml     # Docker build & push
│       ├── image-scan.yml            # Trivy CVE scan
│       └── deploy-to-prod-server.yml # SSH deploy to EC2
└── README.md
```

---

## ✨ Features

- ✅ User registration & login
- ✅ Session-based authentication
- ✅ Password hashing with Flask-Bcrypt
- ✅ Per-user task isolation
- ✅ Auth logging (login / logout / failed attempts)
- ✅ Add, complete, rename, soft-delete todos
- ✅ Persistent MySQL storage
- ✅ Full DevSecOps CI/CD pipeline

---

## ⚙️ Tech Stack

| Layer            | Technology              |
|------------------|-------------------------|
| Frontend         | HTML (Jinja2 Templates) |
| Backend          | Python Flask            |
| Auth             | Flask-Bcrypt + Sessions |
| Database         | MySQL 8.0               |
| Containerization | Docker                  |
| Orchestration    | Docker Compose          |
| CI/CD & Security | GitHub Actions          |
| Hosting          | AWS EC2                 |

---

## 🔐 DevSecOps Pipeline

The pipeline runs automatically on every push to main and on manual trigger (workflow_dispatch).

### Pipeline Flow

```
code-quality + dependency-check + dockerfile-scan + secrets-scan
                          ↓
                   docker-build-push
                          ↓
                       image-scan
                          ↓
               deploy-to-prod-server (EC2)
```

### Pipeline Stages

| Stage | Tool | What it does |
|---|---|---|
| Code Quality | flake8 + bandit | PEP8 linting + SAST security scan |
| Dependency Scan | pip-audit | Checks for CVEs in Python packages |
| Secrets Scan | gitleaks | Detects secrets/credentials in git history |
| Dockerfile Scan | hadolint | Lints Dockerfile for best practices |
| Docker Build & Push | docker/build-push-action | Builds image and pushes to Docker Hub |
| Image Scan | Trivy | Scans Docker image for OS/package CVEs |
| Deploy | appleboy/ssh-action | SSH deploys to EC2 production server |

### GitHub Actions Setup

#### 1. Repository Secrets (Settings → Secrets → Actions)

| Secret | Value |
|---|---|
| `DOCKER_PASSWORD` | Docker Hub access token |
| `PROD_SERVER_HOST` | EC2 public IP address |
| `PROD_SERVER_SSH_KEY` | EC2 private key (full PEM content) |
| `PROD_SERVER_SSH_USER` | EC2 username (e.g. `ubuntu`) |

#### 2. Repository Variables (Settings → Secrets → Variables)

| Variable | Value |
|---|---|
| `DOCKER_USER` | Your Docker Hub username |

#### 3. Self-hosted Runner

All jobs run on a self-hosted runner. To set one up:

```
Repo → Settings → Actions → Runners → New self-hosted runner
```

Follow the instructions to register and start the runner on your EC2 instance.

---

## 🐳 Run with Docker Compose

```bash
# Start the app
docker-compose up -d --build

# Fresh start 
docker-compose down -v
docker-compose up -d --build
```

Useful commands:

```bash
docker-compose ps
docker-compose logs -f
docker-compose down
```

> ⚠️ Never commit `.env` — use environment variables or GitHub Secrets for credentials.

---

## 🖥️ Run Locally (Without Docker)

### Prerequisites
- Python 3.9+
- MySQL 8.0+

```bash
# 1. Setup MySQL
mysql -u root -p
source schema.sql

# 2. Install dependencies
pip install -r requirements.txt

# 3. Set environment variables
export MYSQL_HOST=localhost
export MYSQL_PORT=3306
export MYSQL_USER=root
export MYSQL_PASSWORD=your_password
export MYSQL_DB=mydb
export SECRET_KEY=dev-secret

# 4. Run
python app.py
```

- App: http://localhost:5000
- Health: http://localhost:5000/health


## 🎓 Why This Project Matters

- ✅ Built from scratch — not a copy-paste repo
- ✅ Full DevSecOps pipeline with real security tooling
- ✅ Production-grade auth (bcrypt, session management, audit logging)
- ✅ Demonstrates Docker, CI/CD, and cloud deployment fundamentals
- ✅ Shows security awareness (CVE scanning, secrets detection, SAST)

---

## 📜 License

MIT License — Free to use for learning & portfolio.

---

> **Break things. Fix them. Repeat.**
> That's how real DevOps engineers are made 💪

## ⭐ Final Note

Happy Dockering 🐳🚀