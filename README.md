# University Research Opportunity Portal

**Course:** Computer Networks (CN) &bull; Fall-2026  
**Institution:** National University of Computer & Emerging Sciences (FAST-NUCES), Peshawar Campus  
**Student Name:** Muhammad Ahsan Butt  
**Roll Number:** 24P-0026  
**Section:** BS (AI 5A)  
**GitHub Repository:** [https://github.com/Muhammad-Ahsan-Butt/research-opportunity-portal](https://github.com/Muhammad-Ahsan-Butt/research-opportunity-portal)

---

## 1. Project Overview

The **University Research Opportunity Portal** is a full-stack web application designed to centralize and streamline research openings across academic departments. It replaces scattered noticeboards and chat groups with a unified platform where faculty members can publish, view, update, close, and delete research opportunities, and students can explore and apply.

### System Architecture
* **Backend:** Python (Flask REST API)
* **Database:** MySQL 8.0 (Relational schema with InnoDB engine and utf8mb4 encoding)
* **Frontend:** Responsive Single-Page Application (HTML5, Modern CSS3, JavaScript)
* **API Testing:** Automated Python test suite + Exported Postman and Bruno collections

---

## 2. Directory Structure

```text
research-opportunity-portal/
├── backend/
│   ├── app.py              # Flask server and CRUD REST endpoints
│   ├── db.py               # Database connection manager and initialization
│   └── validators.py       # Input validation rules and error responses
├── database/
│   └── schema.sql          # MySQL database schema and initial seed records
├── frontend/
│   ├── static/
│   │   ├── css/
│   │   │   └── style.css   # Responsive UI styling
│   │   └── js/
│   │       └── app.js      # Frontend controller and REST API client
│   └── templates/
│       └── index.html      # Dashboard and modal dialogs
├── postman/
│   ├── Research_Opportunity_Portal.postman_collection.json # Postman tests
│   └── bruno/              # Bruno API requests collection
├── tests/
│   └── test_api.py         # Automated test suite for all 8 requirements
├── docker-compose.yml      # Multi-container MySQL orchestration
├── package_submission.py   # Script to package submission ZIP
├── requirements.txt        # Python backend dependencies
├── .env.example            # Environment variables template
├── .gitignore              # Git ignore rules
└── README.md               # Project documentation
```

---

## 3. Database Entity Model

The `opportunities` table in MySQL stores all required fields:

| Field Name | Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `id` | `INT` | PRIMARY KEY, AUTO_INCREMENT | Unique opportunity identifier |
| `title` | `VARCHAR(255)` | NOT NULL | Research project title |
| `description` | `TEXT` | NOT NULL | Full project description & objectives |
| `research_area` | `VARCHAR(150)` | NOT NULL | Academic domain / research area |
| `faculty_name` | `VARCHAR(150)` | NOT NULL | Lead faculty supervisor |
| `department` | `VARCHAR(100)` | NOT NULL | Academic department |
| `required_skills` | `TEXT` | NOT NULL | Prerequisites and technical skills |
| `positions_available` | `INT` | NOT NULL, >= 1 | Number of open seats |
| `deadline` | `DATE` | NOT NULL | Application deadline (YYYY-MM-DD) |
| `status` | `ENUM` | NOT NULL, DEFAULT 'Open' | Opportunity state (`Open` or `Closed`) |
| `created_at` | `TIMESTAMP` | DEFAULT CURRENT_TIMESTAMP | Record creation timestamp |
| `updated_at` | `TIMESTAMP` | ON UPDATE CURRENT_TIMESTAMP | Record last update timestamp |

---

## 4. REST API Reference

All API responses are formatted in standard JSON.

### Endpoints Summary

| Method | Endpoint | Description | Status Codes |
| :--- | :--- | :--- | :--- |
| `POST` | `/api/opportunities` | Create a new research opportunity | `201 Created`, `400 Bad Request` |
| `GET` | `/api/opportunities` | Retrieve all research opportunities | `200 OK`, `500 Server Error` |
| `GET` | `/api/opportunities/:id` | Retrieve single opportunity details | `200 OK`, `404 Not Found` |
| `PUT` | `/api/opportunities/:id` | Update opportunity fields or status | `200 OK`, `400 Bad Request`, `404 Not Found` |
| `DELETE` | `/api/opportunities/:id` | Delete an opportunity | `200 OK`, `404 Not Found` |
| `GET` | `/api/health` | Check API and database health | `200 OK`, `500 Unhealthy` |
| `GET` | `/` | Serve frontend dashboard | `200 OK` |

### Sample Payloads

#### `POST /api/opportunities` (Create)
```json
{
  "title": "Autonomous Drone Navigation in GPS-Denied Environments",
  "description": "Visual-inertial SLAM algorithms for aerial robotics.",
  "research_area": "Robotics & Computer Vision",
  "faculty_name": "Dr. Tariq Khan",
  "department": "Computer Science",
  "required_skills": "Python, C++, ROS, OpenCV",
  "positions_available": 2,
  "deadline": "2026-12-31",
  "status": "Open"
}
```

#### `PUT /api/opportunities/:id` (Update or Status Change)
```json
{
  "positions_available": 3,
  "status": "Closed"
}
```

---

## 5. Quickstart & Installation

### Prerequisites
* Python 3.10 or higher
* Docker & Docker Compose (or a local MySQL 8.0 server)

### Step 1: Clone Repository
```bash
git clone https://github.com/Muhammad-Ahsan-Butt/research-opportunity-portal.git
cd research-opportunity-portal
```

### Step 2: Configure Environment
Copy `.env.example` to `.env`:
```bash
cp .env.example .env
```
Default `.env` settings:
```ini
DB_HOST=127.0.0.1
DB_PORT=3306
DB_USER=root
DB_PASSWORD=rootpassword
DB_NAME=research_portal
FLASK_PORT=5000
FLASK_DEBUG=True
```

### Step 3: Start MySQL Database
Using Docker Compose (Recommended):
```bash
docker compose up -d
```
*This starts MySQL 8.0 and automatically runs `database/schema.sql` on startup.*

*(Alternative: If using native MySQL on your system, open MySQL client and run `SOURCE database/schema.sql;`)*

### Step 4: Install Python Dependencies
```bash
pip install -r requirements.txt
```

### Step 5: Start Flask Application
```bash
python backend/app.py
```
Open your browser at **[http://127.0.0.1:5000](http://127.0.0.1:5000)**.

---

## 6. Testing

### Option A: Automated Test Suite (Python)
Run the automated test suite covering all 8 assignment criteria:
```bash
python tests/test_api.py -v
```
All 10 tests verify:
1. Creating Opportunity 1 (`201 Created`)
2. Creating Opportunity 2 (`201 Created`)
3. Creating Opportunity 3 (`201 Created`)
4. Retrieving All Opportunities (`200 OK`)
5. Retrieving Opportunity by ID (`200 OK`)
6. Updating existing opportunity (`200 OK`)
7. Toggling status from Open to Closed (`200 OK`)
8. Deleting an opportunity (`200 OK`)
9. Requesting deleted opportunity (`404 Not Found`)
10. Sending invalid payload missing fields (`400 Bad Request`)

### Option B: Postman Collection
1. Open Postman.
2. Click **Import** and select `postman/Research_Opportunity_Portal.postman_collection.json`.
3. The collection has collection variables `baseUrl = http://127.0.0.1:5000` and dynamically passes IDs between requests.
4. Run individual requests or use **Run collection**.

### Option C: Bruno
1. Open Bruno.
2. Choose **Open Collection** and open the `postman/bruno` folder.
3. Execute the sequenced requests.

---

## 7. 60-Second Demonstration Video Checklist

Follow this order for your 1-minute video demonstration:
1. **Show Backend & Frontend Running (10s):**
   * Show terminal running `python backend/app.py`.
   * Switch to browser at `http://127.0.0.1:5000`.
2. **Display & Retrieve Opportunities (10s):**
   * Scroll through opportunities, show department and status filters.
   * Click **View Details** on an opportunity.
3. **Create New Opportunity (15s):**
   * Click **+ Post Opportunity**, enter sample values, click **Publish Opportunity**.
   * Show the success notification and the new opportunity appearing on the dashboard.
4. **Update & Change Status (10s):**
   * Click **Edit** to update available positions.
   * Click **Mark Closed** to change status from Open to Closed.
5. **Delete & 404 Validation (10s):**
   * Click **Delete**, confirm deletion.
6. **Postman / Bruno Request & Error Response (15s):**
   * Switch to Postman, run `POST /api/opportunities` with missing fields to demonstrate `400 Bad Request`.
   * Send `GET /api/opportunities/<deleted_id>` to demonstrate `404 Not Found`.

---

## 8. Creating Final Submission ZIP

Run the packaging script to generate the submission ZIP file formatted per course guidelines (`P24_0026_MUHAMMAD_AHSAN_BSAI5A.zip`):
```bash
python package_submission.py
```
This packages backend, frontend, database schema, Postman collection, and README into a clean ZIP archive ready for submission.

---

## 9. Troubleshooting

* **MySQL Port Conflict (Port 3306 in use):**
  If port 3306 is occupied by an existing MySQL service, update `docker-compose.yml` to `"3307:3306"` and set `DB_PORT=3307` in `.env`.
* **Database Connection Refused:**
  Ensure container is healthy with `docker ps`. Run `python backend/db.py` to verify connection and table setup.
