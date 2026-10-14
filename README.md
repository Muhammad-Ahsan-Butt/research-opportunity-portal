# University Research Opportunity Portal

**Course:** Computer Networks (CN) - Fall 2026  
**Institution:** FAST-NUCES Peshawar Campus  
**Student Name:** Muhammad Ahsan Butt  
**Roll Number:** 24P-0026  
**Section:** BS (AI 5A)  
**GitHub Repository:** [https://github.com/Muhammad-Ahsan-Butt/research-opportunity-portal](https://github.com/Muhammad-Ahsan-Butt/research-opportunity-portal)  
**Demonstration Video:** `ass-1_demo-video.webm` (included in submission)

---

## Project Overview

A full-stack web application for university faculty members to post and manage research opportunities. Students can browse, view details, and track open/closed research positions across departments.

### Tech Stack
* **Backend:** Python (Flask REST API)
* **Database:** MySQL
* **Frontend:** HTML, CSS, JavaScript (served directly by Flask)

---

## Setup and How to Run

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Start MySQL Database
Using Docker Compose:
```bash
docker compose up -d
```
*(This starts MySQL and automatically loads `database/schema.sql`).*

### 3. Start the Application
```bash
python backend/app.py
```
Open your browser and visit: **http://127.0.0.1:5000**

---

## REST API Endpoints

| Method | Endpoint | Description | Status Code |
| :--- | :--- | :--- | :--- |
| `POST` | `/api/opportunities` | Create new research opportunity | 201 Created |
| `GET` | `/api/opportunities` | Get all research opportunities | 200 OK |
| `GET` | `/api/opportunities/:id` | Get details of a single opportunity | 200 OK / 404 |
| `PUT` | `/api/opportunities/:id` | Update opportunity fields or status | 200 OK / 404 |
| `DELETE` | `/api/opportunities/:id` | Delete an opportunity | 200 OK / 404 |

---

## Testing with Postman

1. Open Postman and click **Import**.
2. Select `postman/Research_Opportunity_Portal.postman_collection.json`.
3. Run the requests to test all CRUD operations, status code 201, 200, 404, and 400 validation error.
