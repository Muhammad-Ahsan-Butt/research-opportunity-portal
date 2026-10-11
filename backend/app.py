"""
Flask REST API for University Research Opportunity Portal
FAST-NUCES Peshawar - Computer Networks Assignment #1
"""

import os
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from dotenv import load_dotenv

from db import get_db_connection, init_db, check_db_connection
from validators import validate_opportunity_payload

load_dotenv()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATE_DIR = os.path.join(BASE_DIR, "frontend", "templates")
STATIC_DIR = os.path.join(BASE_DIR, "frontend", "static")

app = Flask(__name__, template_folder=TEMPLATE_DIR, static_folder=STATIC_DIR)
CORS(app)

# Helper to format date objects in opportunity dictionaries
def serialize_opportunity(row):
    if not row:
        return row
    item = dict(row)
    if "deadline" in item and item["deadline"]:
        item["deadline"] = str(item["deadline"])
    if "created_at" in item and item["created_at"]:
        item["created_at"] = str(item["created_at"])
    if "updated_at" in item and item["updated_at"]:
        item["updated_at"] = str(item["updated_at"])
    return item


# -------------------------------------------------------------
# Error Handlers (Standardized JSON Responses & Status Codes)
# -------------------------------------------------------------
@app.errorhandler(400)
def handle_bad_request(err):
    msg = getattr(err, "description", "Bad Request")
    return jsonify({"success": False, "error": msg}), 400


@app.errorhandler(404)
def handle_not_found(err):
    msg = getattr(err, "description", "Resource not found")
    return jsonify({"success": False, "error": msg}), 404


@app.errorhandler(405)
def handle_method_not_allowed(err):
    return jsonify({"success": False, "error": "Method not allowed on this endpoint."}), 405


@app.errorhandler(500)
def handle_server_error(err):
    return jsonify({"success": False, "error": "Internal server error occurred."}), 500


# -------------------------------------------------------------
# Frontend Route
# -------------------------------------------------------------
@app.route("/", methods=["GET"])
def index():
    """Serve the frontend single-page application."""
    return render_template("index.html")


# -------------------------------------------------------------
# Health Check Endpoint
# -------------------------------------------------------------
@app.route("/api/health", methods=["GET"])
def health_check():
    db_ok = check_db_connection()
    status_code = 200 if db_ok else 500
    return jsonify({
        "status": "healthy" if db_ok else "unhealthy",
        "database_connected": db_ok,
        "service": "University Research Opportunity Portal API"
    }), status_code


# -------------------------------------------------------------
# REST API Endpoints (CRUD)
# -------------------------------------------------------------

# 1. POST /api/opportunities - Create a Research Opportunity
@app.route("/api/opportunities", methods=["POST"])
def create_opportunity():
    try:
        data = request.get_json(silent=True)
        if data is None:
            return jsonify({
                "success": False, 
                "error": "Invalid request. JSON body is required."
            }), 400

        is_valid, error_msg, cleaned = validate_opportunity_payload(data, is_update=False)
        if not is_valid:
            return jsonify({"success": False, "error": error_msg}), 400

        conn = get_db_connection()
        with conn.cursor() as cursor:
            insert_sql = """
                INSERT INTO opportunities (
                    title, description, research_area, faculty_name,
                    department, required_skills, positions_available,
                    deadline, status
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);
            """
            cursor.execute(insert_sql, (
                cleaned["title"],
                cleaned["description"],
                cleaned["research_area"],
                cleaned["faculty_name"],
                cleaned["department"],
                cleaned["required_skills"],
                cleaned["positions_available"],
                cleaned["deadline"],
                cleaned["status"]
            ))
            new_id = cursor.lastrowid

            # Fetch the newly created row
            cursor.execute("SELECT * FROM opportunities WHERE id = %s;", (new_id,))
            created_record = cursor.fetchone()

        conn.close()

        return jsonify({
            "success": True,
            "message": "Research opportunity created successfully.",
            "data": serialize_opportunity(created_record)
        }), 201

    except Exception as exc:
        print(f"[API ERROR] POST /api/opportunities: {exc}")
        return jsonify({"success": False, "error": f"Failed to create opportunity: {str(exc)}"}), 500


# 2. GET /api/opportunities - Retrieve All Research Opportunities
@app.route("/api/opportunities", methods=["GET"])
def get_all_opportunities():
    try:
        status_filter = request.args.get("status")
        department_filter = request.args.get("department")
        search_query = request.args.get("search")

        conditions = []
        params = []

        if status_filter:
            conditions.append("status = %s")
            params.append(status_filter)
        if department_filter:
            conditions.append("department = %s")
            params.append(department_filter)
        if search_query:
            conditions.append("(title LIKE %s OR research_area LIKE %s OR faculty_name LIKE %s)")
            wildcard = f"%{search_query}%"
            params.extend([wildcard, wildcard, wildcard])

        where_clause = f"WHERE {' AND '.join(conditions)}" if conditions else ""
        query = f"SELECT * FROM opportunities {where_clause} ORDER BY id DESC;"

        conn = get_db_connection()
        with conn.cursor() as cursor:
            cursor.execute(query, tuple(params))
            rows = cursor.fetchall()
        conn.close()

        opportunities = [serialize_opportunity(row) for row in rows]
        return jsonify({
            "success": True,
            "count": len(opportunities),
            "data": opportunities
        }), 200

    except Exception as exc:
        print(f"[API ERROR] GET /api/opportunities: {exc}")
        return jsonify({"success": False, "error": f"Failed to retrieve opportunities: {str(exc)}"}), 500


# 3. GET /api/opportunities/:id - Retrieve One Research Opportunity
@app.route("/api/opportunities/<int:opp_id>", methods=["GET"])
def get_opportunity_by_id(opp_id):
    try:
        conn = get_db_connection()
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM opportunities WHERE id = %s;", (opp_id,))
            record = cursor.fetchone()
        conn.close()

        if not record:
            return jsonify({
                "success": False,
                "error": f"Research opportunity with ID {opp_id} not found."
            }), 404

        return jsonify({
            "success": True,
            "data": serialize_opportunity(record)
        }), 200

    except Exception as exc:
        print(f"[API ERROR] GET /api/opportunities/{opp_id}: {exc}")
        return jsonify({"success": False, "error": f"Database error: {str(exc)}"}), 500


# 4. PUT /api/opportunities/:id - Update a Research Opportunity
@app.route("/api/opportunities/<int:opp_id>", methods=["PUT"])
def update_opportunity(opp_id):
    try:
        data = request.get_json(silent=True)
        if data is None:
            return jsonify({
                "success": False,
                "error": "Invalid request. JSON body is required."
            }), 400

        is_valid, error_msg, cleaned = validate_opportunity_payload(data, is_update=True)
        if not is_valid:
            return jsonify({"success": False, "error": error_msg}), 400

        conn = get_db_connection()
        with conn.cursor() as cursor:
            # Check existence first
            cursor.execute("SELECT id FROM opportunities WHERE id = %s;", (opp_id,))
            existing = cursor.fetchone()
            if not existing:
                conn.close()
                return jsonify({
                    "success": False,
                    "error": f"Cannot update. Research opportunity with ID {opp_id} not found."
                }), 404

            # Build dynamic UPDATE clause
            set_clauses = [f"{col} = %s" for col in cleaned.keys()]
            update_sql = f"UPDATE opportunities SET {', '.join(set_clauses)} WHERE id = %s;"
            params = list(cleaned.values()) + [opp_id]

            cursor.execute(update_sql, tuple(params))

            # Fetch updated record
            cursor.execute("SELECT * FROM opportunities WHERE id = %s;", (opp_id,))
            updated_record = cursor.fetchone()

        conn.close()

        return jsonify({
            "success": True,
            "message": "Research opportunity updated successfully.",
            "data": serialize_opportunity(updated_record)
        }), 200

    except Exception as exc:
        print(f"[API ERROR] PUT /api/opportunities/{opp_id}: {exc}")
        return jsonify({"success": False, "error": f"Failed to update opportunity: {str(exc)}"}), 500


# 5. DELETE /api/opportunities/:id - Delete a Research Opportunity
@app.route("/api/opportunities/<int:opp_id>", methods=["DELETE"])
def delete_opportunity(opp_id):
    try:
        conn = get_db_connection()
        with conn.cursor() as cursor:
            # Check existence
            cursor.execute("SELECT id, title FROM opportunities WHERE id = %s;", (opp_id,))
            existing = cursor.fetchone()
            if not existing:
                conn.close()
                return jsonify({
                    "success": False,
                    "error": f"Cannot delete. Research opportunity with ID {opp_id} not found."
                }), 404

            cursor.execute("DELETE FROM opportunities WHERE id = %s;", (opp_id,))

        conn.close()

        return jsonify({
            "success": True,
            "message": f"Research opportunity #{opp_id} ('{existing['title']}') was deleted successfully."
        }), 200

    except Exception as exc:
        print(f"[API ERROR] DELETE /api/opportunities/{opp_id}: {exc}")
        return jsonify({"success": False, "error": f"Failed to delete opportunity: {str(exc)}"}), 500


# -------------------------------------------------------------
# Main Application Runner
# -------------------------------------------------------------
if __name__ == "__main__":
    port = int(os.getenv("FLASK_PORT", 5000))
    debug = os.getenv("FLASK_DEBUG", "True").lower() in ("true", "1", "yes")

    print("[STARTUP] Checking database initialization...")
    try:
        init_db()
        print("[STARTUP] Database verified.")
    except Exception as e:
        print(f"[STARTUP WARNING] Database auto-check: {e}")

    print(f"Starting Research Opportunity Portal on http://127.0.0.1:{port}")
    app.run(host="0.0.0.0", port=port, debug=debug)
