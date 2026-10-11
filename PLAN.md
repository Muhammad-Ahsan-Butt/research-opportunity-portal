# 10-Step Implementation Plan: University Research Opportunity Portal

## Overview
This plan outlines the 10-step phased implementation of the University Research Opportunity Portal for Computer Networks Assignment #1. Each step is self-contained, verifiable, and paired with human-readable Git commits.

---

### Step 1: Project Structure & Environment Initialization
* **Goal**: Establish a clean repository architecture and configure Python dependencies.
* **Tasks**:
  * Set up directory structure:
    * `backend/` (Flask app, routes, DB connection)
    * `database/` (SQL schema and seed data)
    * `frontend/` (Templates, static CSS, JS)
    * `postman/` (Postman and Bruno test collections)
  * Create `requirements.txt` (`Flask`, `Flask-Cors`, `PyMySQL`, `python-dotenv`, `cryptography`).
  * Create `.gitignore` for Python, virtual environments, `.env`, and OS caches.
* **Verification**: Verify virtual environment installation and dependencies without errors.
* **Git Commit**: `"Initialize project folder structure, dependencies, and gitignore"`

---

### Step 2: MySQL Database Schema & Containerization Setup
* **Goal**: Define the relational schema satisfying all required entity fields and provide an instant setup method.
* **Tasks**:
  * Create `database/schema.sql`:
    * Table `opportunities` with: `id` (INT PK AUTO_INCREMENT), `title`, `description`, `research_area`, `faculty_name`, `department`, `required_skills`, `positions_available`, `deadline`, `status` (ENUM('Open', 'Closed') or VARCHAR), `created_at`, `updated_at`.
  * Create `docker-compose.yml` for spinning up MySQL 8.0 on port `3306` with automatic schema mounting into `/docker-entrypoint-initdb.d/`.
  * Create `.env.example` and `.env` with DB credentials (`DB_HOST`, `DB_USER`, `DB_PASSWORD`, `DB_NAME`, `DB_PORT`).
* **Verification**: Start MySQL container, connect, and verify table schema matches specification.
* **Git Commit**: `"Add MySQL database schema and docker-compose configuration"`

---

### Step 3: Database Connection Module & Resilience
* **Goal**: Build a robust database abstraction layer with connection pooling and schema verification.
* **Tasks**:
  * Create `backend/db.py`:
    * Uses `pymysql` with `DictCursor` for JSON-friendly dictionary output.
    * Connection helper `get_db_connection()`.
    * Helper `init_db()` to auto-create database/table if not already present on server startup.
    * Database health-check function.
* **Verification**: Run a standalone test script to test DB connection and verify tables exist.
* **Git Commit**: `"Implement database connection manager and table initialization logic"`

---

### Step 4: Input Validation & Error Handling Layer
* **Goal**: Ensure reliable input sanitization and correct HTTP status code generation.
* **Tasks**:
  * Create `backend/validators.py`:
    * Validate mandatory fields: `title`, `description`, `research_area`, `faculty_name`, `department`, `required_skills`, `positions_available`, `deadline`, `status`.
    * Validate data types (e.g., `positions_available` is a positive integer, `status` in `['Open', 'Closed']`, `deadline` format `YYYY-MM-DD`).
    * Return standardized error response structures: `{"success": false, "error": "Reason"}`.
  * Standardize status codes:
    * `200 OK` (successful retrieval/update/delete)
    * `201 Created` (successful creation)
    * `400 Bad Request` (missing or invalid fields)
    * `404 Not Found` (resource does not exist)
    * `500 Internal Server Error` (database/server error)
* **Verification**: Unit tests on validation helper functions.
* **Git Commit**: `"Add input validation rules and standardized error handling"`

---

### Step 5: Backend REST API Endpoints Implementation
* **Goal**: Implement all 5 mandatory CRUD endpoints in Flask.
* **Tasks**:
  * Create `backend/app.py`:
    * `POST /api/opportunities`: Validate body, insert row, return `201 Created` with created record.
    * `GET /api/opportunities`: Fetch all opportunities ordered by creation date, return `200 OK`.
    * `GET /api/opportunities/<int:id>`: Fetch single record by ID; return `404 Not Found` if missing, otherwise `200 OK`.
    * `PUT /api/opportunities/<int:id>`: Validate body, update fields, return `200 OK`, or `404 Not Found` if missing.
    * `DELETE /api/opportunities/<int:id>`: Check existence, delete row, return `200 OK` or `404 Not Found`.
    * Serve frontend entrypoint route (`GET /`).
* **Verification**: Start Flask app, check server binding on `http://localhost:5000`.
* **Git Commit**: `"Implement complete CRUD REST API endpoints for research opportunities"`

---

### Step 6: Backend API Testing (Covering All 8 Test Scenarios)
* **Goal**: Verify API against all 8 assignment criteria using automated test requests.
* **Tasks**:
  * Create automated test suite `tests/test_api.py` covering:
    1. Create Opportunity #1 (`201`)
    2. Create Opportunity #2 (`201`)
    3. Create Opportunity #3 (`201`)
    4. Retrieve All Opportunities (`200`)
    5. Retrieve One Opportunity by ID (`200`)
    6. Update Opportunity details (`200`)
    7. Change status from Open to Closed (`200`)
    8. Delete Opportunity (`200`)
    9. Request deleted Opportunity to confirm `404 Not Found`
    10. Submit invalid payload to confirm `400 Bad Request`
* **Verification**: Execute test suite and ensure 100% test pass rate.
* **Git Commit**: `"Add comprehensive automated test suite for all 8 required API scenarios"`

---

### Step 7: Frontend Layout & UI Component Design
* **Goal**: Build a clean, responsive web interface for managing research opportunities.
* **Tasks**:
  * Create `frontend/templates/index.html`:
    * University header & portal branding.
    * Action toolbar (Search bar, Department filter, Status filter, "Add Opportunity" button).
    * Opportunity grid container with clean empty and loading states.
    * Modal for "Create New Opportunity".
    * Modal for "Edit Opportunity".
    * Modal for "Opportunity Details View".
    * Confirmation modal for "Delete Opportunity".
    * Toast notification container.
  * Create `frontend/static/css/style.css`:
    * Responsive layout, modern card aesthetics, clean typography, badge indicators for Open/Closed status.
* **Verification**: Open UI in browser and verify layout, modals, and responsive styling.
* **Git Commit**: `"Design modern and responsive frontend UI layout and modals"`

---

### Step 8: Frontend Client Logic & API Integration
* **Goal**: Connect frontend to backend REST API with real-time updates and interactive UX.
* **Tasks**:
  * Create `frontend/static/js/app.js`:
    * `loadOpportunities()`: Fetch from `GET /api/opportunities` and render dynamic cards.
    * Client-side search and filtering by department & status.
    * `handleCreateOpportunity()`: Collect form data, submit to `POST /api/opportunities`, display toast notification, refresh list.
    * `handleEditOpportunity()`: Populate modal with existing values, submit to `PUT /api/opportunities/:id`.
    * `toggleStatus()`: One-click status switch (`Open` <-> `Closed`) via `PUT /api/opportunities/:id`.
    * `handleDeleteOpportunity()`: Prompt confirmation and send `DELETE /api/opportunities/:id`.
    * `viewOpportunityDetails()`: Display full description and info in details modal.
    * Client-side form validation before dispatching requests.
* **Verification**: Full manual interaction in browser verifying create, read, update, status toggle, delete, and notifications.
* **Git Commit**: `"Connect frontend JavaScript to REST API with CRUD operations and live feedback"`

---

### Step 9: Postman & Bruno Test Collection Export
* **Goal**: Provide ready-to-import Postman and Bruno test collections for evaluation.
* **Tasks**:
  * Create `postman/Research_Opportunity_Portal.postman_collection.json` containing:
    * Environment variable setup (`{{baseUrl}} = http://localhost:5000`).
    * Request 1: `POST /api/opportunities` (Create opportunity 1)
    * Request 2: `POST /api/opportunities` (Create opportunity 2)
    * Request 3: `POST /api/opportunities` (Create opportunity 3)
    * Request 4: `GET /api/opportunities` (Get all)
    * Request 5: `GET /api/opportunities/1` (Get one by ID)
    * Request 6: `PUT /api/opportunities/1` (Update opportunity)
    * Request 7: `PUT /api/opportunities/1` (Change status to Closed)
    * Request 8: `DELETE /api/opportunities/1` (Delete opportunity)
    * Request 9: `GET /api/opportunities/1` (Expect 404 Not Found)
    * Request 10: `POST /api/opportunities` (Invalid data - Expect 400 Bad Request)
    * Pre-configured test assertions for status codes in Postman.
  * Also generate a Bruno collection folder in `postman/bruno-collection/` for students/teachers using Bruno.
* **Verification**: Test requests using command-line collection runner or import test.
* **Git Commit**: `"Add exported Postman and Bruno API test collections covering all 8 requirements"`

---

### Step 10: Documentation, Packaging & Final Review
* **Goal**: Deliver a submission-ready package with clear instructions.
* **Tasks**:
  * Create `README.md`:
    * Project overview and architecture.
    * Prerequisites (Python, MySQL / Docker).
    * Step-by-step setup and run instructions.
    * REST API documentation table (Endpoints, methods, payload, status codes).
    * Postman / Bruno import guide.
    * GitHub repository link placeholder.
    * Step-by-step script guide for the 1-minute video demonstration.
  * Provide zip packaging script to produce `P24_0000_NAME_CLASS.zip` adhering to Section 8 of the assignment.
* **Verification**: Verify clean startup from scratch using only instructions in `README.md`.
* **Git Commit**: `"Add comprehensive README documentation and submission packaging guide"`
