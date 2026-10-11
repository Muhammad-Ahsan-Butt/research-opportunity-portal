# Assignment No. 1: University Research Opportunity Portal
**National University of Computer & Emerging Sciences (FAST-NUCES), Peshawar Campus**  
**Program:** BS (AI 5A) | **Semester:** Fall-2026 | **Course:** Computer Networks (CN)

---

## 1. Scenario
Your university currently shares research opportunities through emails, WhatsApp groups, and noticeboards. Because information is scattered, many students miss valuable opportunities while faculty members find it difficult to manage their openings.
The university has decided to develop a **Research Opportunity Portal** where faculty members can post, view, update, and manage research opportunities in one place.

You are working as a junior software developer in the university's software development team. Your responsibility is to develop a complete web-based application consisting of a **backend REST API**, **database**, and a **frontend interface** for managing research opportunities.

---

## 2. Backend Requirements
Develop a backend REST API that allows faculty members to perform CRUD operations on research opportunities.

Each research opportunity must contain the following information:
1. **Unique ID**
2. **Research title**
3. **Research description**
4. **Research area**
5. **Faculty member's name**
6. **Department**
7. **Required skills**
8. **Number of available positions**
9. **Application deadline**
10. **Status:** `Open` or `Closed`

### Endpoints to Implement:
* **2.1 Create a Research Opportunity**
  * `POST /api/opportunities`
  * Create and store a new research opportunity in the database.
* **2.2 Retrieve All Research Opportunities**
  * `GET /api/opportunities`
  * Return all research opportunities stored in the database.
* **2.3 Retrieve One Research Opportunity**
  * `GET /api/opportunities/:id`
  * Return the complete details of a specific opportunity using its ID.
* **2.4 Update a Research Opportunity**
  * `PUT /api/opportunities/:id`
  * Update an existing opportunity, such as title, required skills, positions, deadline, or status.
* **2.5 Delete a Research Opportunity**
  * `DELETE /api/opportunities/:id`
  * Delete a research opportunity that was posted by mistake or is no longer required.

### 2.6 Status Codes:
Students must use appropriate HTTP status codes, including:
* `200 OK`
* `201 Created`
* `400 Bad Request`
* `404 Not Found`
* `500 Internal Server Error`

---

## 3. Frontend Requirements
Students must develop a frontend interface for interacting with the backend API.
The frontend should provide the following functionality:
1. Display all available research opportunities.
2. Display complete details of a selected research opportunity.
3. Provide a form for creating a new research opportunity.
4. Provide an option to update an existing research opportunity.
5. Allow the status of an opportunity to be changed from `Open` to `Closed`.
6. Provide an option to delete a research opportunity.
7. Display appropriate success and error messages.
8. Perform basic validation for required form fields.

* Note: The frontend must communicate with the backend through the implemented REST API. Data should not be hard-coded. A simple, clean, and functional interface is sufficient.

---

## 4. Technologies
* **4.1 Backend:** Python, Java, or JavaScript / Node.js
* **4.2 Database:** MySQL
* **4.3 Frontend:** HTML, CSS, JavaScript, Bootstrap, or React.js

---

## 5. GitHub Repository
* Complete project in GitHub repository: Backend source code, Frontend source code, Database schema/setup files, `README.md`, Exported Postman/Bruno collection.
* Make meaningful Git commits while developing the project (not a single bulk commit).
* Repository link must be included in `README.md`.
* Do not upload passwords, API keys, or private credentials.

---

## 6. Postman or Bruno Testing
Demonstration test suite must include:
1. Creating at least three research opportunities.
2. Retrieving all research opportunities.
3. Retrieving one opportunity using its ID.
4. Updating an existing opportunity.
5. Changing an opportunity's status from `Open` to `Closed`.
6. Deleting an opportunity.
7. Requesting the deleted opportunity again to demonstrate a `404 Not Found` response.
8. Sending one request containing invalid or missing data to demonstrate input validation (`400 Bad Request`).
* Export Postman or Bruno collection and include it in final submission & GitHub repository.

---

## 7. One-Minute Demonstration Video
Record a ~1 minute video demonstrating:
* Backend server running.
* Frontend application running.
* Creating, retrieving, updating, closing, deleting an opportunity.
* Displaying at least one validation or 404 error.
* API requests and responses in Postman or Bruno.

---

## 8. Submission Requirements
Submit one ZIP file named: `P24_0000_NAME_CLASS.zip` containing:
* Complete frontend and backend source code
* Database setup/schema
* Exported Postman or Bruno collection
* `README.md` with setup and run instructions
* GitHub repository link
* Video file or link

---

## 9. Important Instructions
* Individual assignment.
* Both frontend and backend are required.
* All CRUD operations must use the database (no hard-coded data).
* Project must run using instructions in `README.md`.
