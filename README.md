# 🚀 Two-Tier Application (Flask + MySQL) – Docker Practice Project

A hands-on two-tier web application built with Flask (backend) and MySQL (database). This repository is designed purely for learning and practising Docker & DevOps concepts step by step — from basic Dockerfiles to Docker Compose and CI/CD.

> 🎯 **Goal:** Learn Docker by *building everything yourself* instead of just running ready-made configs.

---

## 🧩 Application Overview

This is a simple **Todo List application** where:

* Users can add tasks
* Mark tasks as completed
* Delete tasks
* All data is stored persistently in MySQL

The app follows a **two-tier architecture**:

```
Client (Browser)
      ↓
Flask App (Backend)
      ↓
MySQL Database
```

---

## 🗂️ Project Structure

```
two-tier-app/
├── app.py                  # Flask application logic
├── requirements.txt        # Python dependencies
├── schema.sql              # MySQL schema
├── templates/
│   └── index.html          # Frontend UI
├── README.md               # Project documentation
├── DOCKER_PRACTICE_GUIDE.md# Docker learning roadmap

# Files YOU will create during practice 👇
├── Dockerfile
├── .dockerignore
├── docker-compose.yml
├── .env
└── Jenkinsfile (optional)
```

---

## ✨ Features

* ✅ Add todos
* ✅ Mark todos as completed
* ✅ Delete todos
* ✅ Persistent storage using MySQL
* ✅ Health check endpoint
* ✅ Clean & simple UI

---

## ⚙️ Tech Stack

| Layer            | Technology             |
| ---------------- | ---------------------- |
| Frontend         | HTML (Jinja Templates) |
| Backend          | Python Flask           |
| Database         | MySQL 8.0              |
| Containerization | Docker                 |
| Orchestration    | Docker Compose         |
| CI/CD (Optional) | Jenkins                |

---

## 🚀 Run Without Docker (Local Setup)

### Prerequisites

* Python 3.9+
* MySQL 8.0+

### 1️⃣ Setup MySQL

```bash
mysql -u root -p
source schema.sql
```

### 2️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 3️⃣ Set Environment Variables

```bash
export MYSQL_HOST=localhost
export MYSQL_PORT=3306
export MYSQL_USER=root
export MYSQL_PASSWORD=your_password
export MYSQL_DB=todo_db
export SECRET_KEY=dev-secret
```

### 4️⃣ Run Application

```bash
python app.py
```

📍 Access:

* App: [http://localhost:5000](http://localhost:5000)
* Health: [http://localhost:5000/health](http://localhost:5000/health)

---

## 🐳 Docker Learning Roadmap

This repository is intentionally **Docker-first learning focused**.

📌 Refer to **DOCKER_PRACTICE_GUIDE.md** for detailed steps.

### Learning Phases

1. 🧱 **Basic Dockerfile**
2. 🏗️ **Multi-stage Docker builds**
3. 🔒 **Distroless images**
4. 💾 **Docker volumes (MySQL persistence)**
5. 🌐 **Docker networking**
6. 🎼 **Docker Compose orchestration**
7. 🏷️ **Image tagging & versioning**
8. 📤 **Push images to Docker Hub**
9. 🔄 **CI/CD with Jenkins**

---

## 🐙 Run with Docker Compose (After Practice)

```bash
docker-compose up -d
```

Useful commands:

```bash
docker-compose ps
docker-compose logs -f
docker-compose down
docker-compose down -v
```

<img width="1600" height="880" alt="image" src="https://github.com/user-attachments/assets/a3874fd6-917d-4c02-8970-3664710c2bb9" />

---

## 🔑 Environment Variables

| Variable       | Description       |
| -------------- | ----------------- |
| MYSQL_HOST     | Database hostname |
| MYSQL_PORT     | MySQL port        |
| MYSQL_USER     | DB username       |
| MYSQL_PASSWORD | DB password       |
| MYSQL_DB       | Database name     |
| SECRET_KEY     | Flask secret key  |

---

## 🔌 API Endpoints

| Method | Endpoint       | Description        |
| ------ | -------------- | ------------------ |
| GET    | /              | View all todos     |
| POST   | /add           | Add new todo       |
| GET    | /complete/<id> | Mark todo complete |
| GET    | /delete/<id>   | Delete todo        |
| GET    | /health        | Health check       |

---

## 🐞 Common Issues & Fixes

### ❌ Database Connection Error

* Ensure MySQL container is running
* Wait ~30 seconds for DB initialisation
* Verify environment variables

### ❌ Port Already in Use

```bash
docker run -p 5001:5000 flask-app
```

### ❌ Docker Permission Denied

```bash
sudo usermod -aG docker $USER
```

(Re-login required)

---

## 💡 Best Practices Learned

* ✔ Writing optimised Dockerfiles
* ✔ Using `.dockerignore`
* ✔ Multi-stage builds for smaller images
* ✔ Persistent data using volumes
* ✔ Service discovery via Docker networking
* ✔ Environment-based configuration
* ✔ CI/CD basics

---

## 🎓 Why This Project Matters (Interview POV)

✅ Built from scratch
✅ Not a copy-paste repo
✅ Explains **how Docker actually works**
✅ Demonstrates real DevOps fundamentals

** Final app deployement will look like :- 

<img width="1140" height="1102" alt="image" src="https://github.com/user-attachments/assets/f371ca61-88e8-4e6e-904a-126763b16c5f" />


> Interviewers value **understanding**, not just running commands.

---

## 📈 What You Can Add Next

* Kubernetes deployment
* GitHub Actions CI/CD
* Nginx reverse proxy
* Prometheus & Grafana
* AWS ECS deployment

---

## 📜 License

MIT License — Free to use for learning & portfolio.

---

## ⭐ Final Note

> **Break things. Fix them. Repeat.**

That’s how real DevOps engineers are made 💪

Happy Dockering 🐳🚀
