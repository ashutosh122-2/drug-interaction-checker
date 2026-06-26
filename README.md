# 💊 Drug Interaction Checker

> An AI-powered web application that detects drug interactions using a Neo4j Knowledge Graph and Machine Learning, with an interactive React frontend and FastAPI backend.

![Python](https://img.shields.io/badge/Python-3.12-blue?style=for-the-badge&logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-Backend-009688?style=for-the-badge&logo=fastapi)
![React](https://img.shields.io/badge/React-Frontend-61DAFB?style=for-the-badge&logo=react)
![Neo4j](https://img.shields.io/badge/Neo4j-Aura-008CC1?style=for-the-badge&logo=neo4j)
![Machine Learning](https://img.shields.io/badge/Machine-Learning-orange?style=for-the-badge)
![License](https://img.shields.io/badge/Status-Active-success?style=for-the-badge)

---

## 📖 Overview

Medication safety is one of the biggest challenges in healthcare. Certain drug combinations can reduce effectiveness or even cause serious adverse effects.

This project was built to make checking drug interactions simple, interactive, and intelligent.

Users can search for two medicines, instantly check whether they interact, visualize their relationship using a knowledge graph, and even receive an AI prediction when an interaction is not found in the database.

The project combines **Knowledge Graphs**, **Machine Learning**, and a modern **Full Stack Web Application** into a single platform.

---

# ✨ Features

- 🔍 Drug Autocomplete Search
- 💊 Drug Interaction Detection
- 🤖 AI-Based Severity Prediction
- 📊 Risk Score Calculation
- 🌐 Neo4j Knowledge Graph
- 📈 Interactive Graph Visualization
- 🕒 Recent Search History
- 📊 Dashboard Statistics
- ⚡ FastAPI REST APIs
- 🎨 Responsive React Interface

---

# 🏗️ System Architecture

```text
                User
                  │
                  ▼
          React Frontend
                  │
         REST API Requests
                  │
                  ▼
          FastAPI Backend
          ├──────────────┐
          │              │
          ▼              ▼
     Neo4j Aura      ML Model
 Knowledge Graph   (Random Forest)
```

---

# 🛠 Tech Stack

## Frontend

- React
- React Flow
- JavaScript
- CSS

## Backend

- FastAPI
- Python

## Database

- Neo4j Aura
- Cypher Query Language

## Machine Learning

- Scikit-Learn
- Random Forest Classifier
- TF-IDF Vectorizer
- Joblib

## Tools

- Git
- GitHub
- VS Code

---

# 📂 Project Structure

```text
drug-interaction-checker/
│
├── backend/
│   ├── app/
│   │   ├── database.py
│   │   ├── main.py
│   │   └── ml_model.py
│
├── frontend/
│   ├── src/
│   └── public/
│
├── scripts/
│
├── data/
│   └── drug_interactions.csv
│
├── README.md
└── .gitignore
```

---

# 🚀 Key Functionalities

### 🔍 Drug Search

Searches medicines with autocomplete support powered by Neo4j.

---

### 💊 Drug Interaction Checker

Checks whether two drugs interact using the Knowledge Graph.

Returns:

- Severity
- Risk Score
- Interaction Description

---

### 🤖 AI Prediction

If the interaction does not exist inside Neo4j, the Machine Learning model predicts the possible severity.

---

### 🌐 Knowledge Graph

Drug relationships are visualized using React Flow.

Each graph displays

- Drug Nodes
- Interaction Edge
- Interaction Description

---

### 📊 Dashboard

Displays

- Total Drugs
- Total Drug Interactions
- AI Model Status

---

### 🕒 Recent Searches

The application stores recent searches locally for quick access.

---

# 📡 API Endpoints

| Method | Endpoint | Description |
|---------|----------|-------------|
| GET | `/` | API Status |
| GET | `/drugs/count` | Total Drugs |
| GET | `/drug/{drug_name}` | Search Drug |
| GET | `/drugs/search` | Autocomplete Search |
| GET | `/interaction` | Check Drug Interaction |
| GET | `/dashboard/stats` | Dashboard Statistics |
| GET | `/graph` | Graph Visualization |

---

# ⚙️ Installation

## Clone Repository

```bash
git clone https://github.com/ashutosh122-2/drug-interaction-checker.git

cd drug-interaction-checker
```

---

## Backend Setup

```bash
python -m venv .venv

source .venv/bin/activate
```

Windows

```bash
.venv\Scripts\activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

Run Backend

```bash
uvicorn backend.app.main:app --reload
```

---

## Frontend Setup

```bash
cd frontend

npm install

npm run dev
```

---

# 📷 Screenshots

> Add screenshots here after deployment.

Suggested screenshots:

- Dashboard
- Autocomplete Search
- Interaction Result
- Graph Visualization
- AI Prediction

---

# 🎯 Future Improvements

- User Authentication
- Drug Recommendation System
- Prescription Upload
- PDF Report Generation
- Multi-Hop Drug Relationships
- Explainable AI
- Medical Ontology Integration
- Docker Deployment
- CI/CD Pipeline
- Cloud Monitoring

---

# 📈 Dataset

The project uses a curated dataset containing drug interaction information.

- Total Drugs: **1701**
- Total Interactions: **191,252**

---

# 💡 What I Learned

While building this project, I gained hands-on experience with:

- Designing REST APIs using FastAPI
- Working with Graph Databases (Neo4j Aura)
- Building Knowledge Graphs
- Creating Machine Learning pipelines
- Integrating ML with a Full Stack application
- React state management
- API integration
- Graph visualization
- Git & GitHub workflows

---

# 👨‍💻 Author

**Ashutosh Shukla**

B.Tech CSE (AI & ML)

GitHub:
https://github.com/ashutosh122-2

LinkedIn:
https://www.linkedin.com/in/01ashutosh09

---

## ⭐ Support

If you found this project useful, consider giving it a ⭐ on GitHub.

It motivates me to keep learning and building better software.