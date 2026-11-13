
import os
import sqlite3
import requests
from pathlib import Path
from flask import Flask, jsonify, request, render_template

app = Flask(__name__)

# ==========================================
# DATABASE CONNECTION
# ==========================================

BASE_DIR = Path(__file__).resolve().parent
DATABASE = BASE_DIR / "students.db"

CLASSMATE_API_URL = os.environ.get(
    "CLASSMATE_API_URL",
    "https://rubyjoymolina-2.onrender.com/api/students"
).strip()

if not CLASSMATE_API_URL:
    CLASSMATE_API_URL = "https://rubyjoymolina-2.onrender.com/api/students"


def get_db_connection():
    conn = sqlite3.connect(str(DATABASE))
    conn.row_factory = sqlite3.Row
    return conn


# ==========================================
# HOME PAGE
# ==========================================

@app.route("/")
def home():
    return render_template("index.html")


# ==========================================
# EXISTING STUDENT API
# ==========================================

@app.route("/student")
def get_student():
    return jsonify({
        "student_id": "24-00228",
        "name": "Josil Paclibar",
        "program": "BSIT",
        "year": 3,
        "section": "Dijkstra"
    })


@app.route("/hello")
def say_hello():
    name = request.args.get("name", "Student")
    return jsonify({"message": f"Hello, {name}!"})


@app.route("/course")
def get_course():
    return jsonify({
        "course_code": "IT 3120",
        "course_title": "Information Technology",
        "instructor": "Rene Ardou",
        "semester": "First Semester",
        "academic_year": "2026-2027"
    })


# ==========================================
# ACTIVITY 7 - STUDENTS
# ==========================================

@app.route("/students", methods=["GET"])
def get_students():
    try:
        with get_db_connection() as conn:
            students = conn.execute(
                "SELECT * FROM students"
            ).fetchall()

        return jsonify([dict(student) for student in students])

    except sqlite3.Error:
        app.logger.exception("Could not retrieve students")
        return jsonify({"error": "Database query failed"}), 500


@app.route("/students/<int:id>", methods=["GET"])
def get_student_by_id(id):
    try:
        with get_db_connection() as conn:
            student = conn.execute(
                "SELECT * FROM students WHERE id = ?", (id,)
            ).fetchone()

        if student is None:
            return jsonify({"error": "Student not found"}), 404

        return jsonify(dict(student))

    except sqlite3.Error:
        app.logger.exception("Could not retrieve student")
        return jsonify({"error": "Database query failed"}), 500


@app.route("/students/section/<section>", methods=["GET"])
def get_students_by_section(section):
    try:
        with get_db_connection() as conn:
            students = conn.execute(
                "SELECT * FROM students WHERE section = ?",
                (section,)
            ).fetchall()

        return jsonify([dict(student) for student in students])

    except sqlite3.Error:
        app.logger.exception("Could not retrieve section records")
        return jsonify({"error": "Database query failed"}), 500


# ==========================================
# ACTIVITY 8 - GET ALL STUDENTS
# ==========================================

@app.route("/api/students", methods=["GET"])
def api_get_students():
    try:
        with get_db_connection() as conn:
            students = conn.execute(
                "SELECT * FROM students"
            ).fetchall()

        return jsonify([dict(student) for student in students])

    except sqlite3.Error:
        app.logger.exception("Could not retrieve API students")
        return jsonify({"error": "Database query failed"}), 500


# ==========================================
# ACTIVITY 8 AND 9 - ADD STUDENT
# ==========================================

@app.route("/api/students", methods=["POST"])
def api_add_student():
    data = request.get_json(silent=True)

    if not data:
        return jsonify({"error": "JSON data is required"}), 400

    required_fields = [
        "student_id", "name", "program", "year", "section"
    ]

    for field in required_fields:
        if field not in data or str(data[field]).strip() == "":
            return jsonify({"error": f"{field} is required"}), 400

    try:
        year = int(data["year"])
    except (ValueError, TypeError):
        return jsonify({"error": "Year must be a number"}), 400

    source = data.get("source", "External API")

    try:
        with get_db_connection() as conn:
            cursor = conn.execute(
                """
                INSERT INTO students
                (student_id, name, program, year, section, source)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    data["student_id"],
                    data["name"],
                    data["program"],
                    year,
                    data["section"],
                    source
                )
            )

            new_id = cursor.lastrowid

        return jsonify({
            "message": "Student added successfully",
            "id": new_id,
            "source": source
        }), 201

    except sqlite3.IntegrityError:
        return jsonify({"error": "Student record already exists"}), 409

    except sqlite3.Error:
        app.logger.exception("Could not add student")
        return jsonify({"error": "Database insert failed"}), 500


# ==========================================
# ACTIVITY 8 - GET ONE STUDENT
# ==========================================

@app.route("/api/students/<int:id>", methods=["GET"])
def api_get_student(id):
    try:
        with get_db_connection() as conn:
            student = conn.execute(
                "SELECT * FROM students WHERE id = ?", (id,)
            ).fetchone()

        if student is None:
            return jsonify({"error": "Student not found"}), 404

        return jsonify(dict(student))

    except sqlite3.Error:
        app.logger.exception("Could not retrieve API student")
        return jsonify({"error": "Database query failed"}), 500


# ==========================================
# ACTIVITY 8 - UPDATE STUDENT
# ==========================================

@app.route("/api/students/<int:id>", methods=["PUT"])
def api_update_student(id):
    data = request.get_json(silent=True)

    if not data:
        return jsonify({"error": "JSON data is required"}), 400

    allowed_fields = [
        "student_id", "name", "program", "year", "section", "source"
    ]

    updates = {
        key: data[key]
        for key in allowed_fields
        if key in data
    }

    if not updates:
        return jsonify({"error": "No valid fields provided"}), 400

    if "year" in updates:
        try:
            updates["year"] = int(updates["year"])
        except (ValueError, TypeError):
            return jsonify({"error": "Year must be a number"}), 400

    try:
        with get_db_connection() as conn:
            student = conn.execute(
                "SELECT id FROM students WHERE id = ?", (id,)
            ).fetchone()

            if student is None:
                return jsonify({"error": "Student not found"}), 404

            set_clause = ", ".join(
                f"{field} = ?" for field in updates
            )

            values = list(updates.values()) + [id]

            conn.execute(
                f"UPDATE students SET {set_clause} WHERE id = ?",
                values
            )

        return jsonify({"message": "Student updated successfully"})

    except sqlite3.IntegrityError:
        return jsonify({"error": "Duplicate student record"}), 409

    except sqlite3.Error:
        app.logger.exception("Could not update student")
        return jsonify({"error": "Database update failed"}), 500


# ==========================================
# ACTIVITY 8 - DELETE STUDENT
# ==========================================

@app.route("/api/students/<int:id>", methods=["DELETE"])
def api_delete_student(id):
    try:
        with get_db_connection() as conn:
            result = conn.execute(
                "DELETE FROM students WHERE id = ?", (id,)
            )
            deleted = result.rowcount

        if deleted == 0:
            return jsonify({"error": "Student not found"}), 404

        return jsonify({"message": "Student deleted successfully"})

    except sqlite3.Error:
        app.logger.exception("Could not delete student")
        return jsonify({"error": "Database delete failed"}), 500


# ==========================================
# ACTIVITY 9 - RETRIEVE CLASSMATE RECORDS
# ==========================================

@app.route("/partner-records", methods=["GET"])
@app.route("/api/classmates", methods=["GET"])
def get_classmate_records():

    if not CLASSMATE_API_URL:
        return jsonify({
            "error": "Classmate API URL is not configured"
        }), 503

    try:
        response = requests.get(
            CLASSMATE_API_URL,
            timeout=15
        )
        response.raise_for_status()

        return jsonify(response.json()), 200

    except requests.RequestException as error:
        app.logger.exception("Could not retrieve classmate records")
        return jsonify({
            "error": "Unable to retrieve classmate records",
            "details": str(error)
        }), 502

    except ValueError:
        return jsonify({
            "error": "Classmate API returned invalid JSON"
        }), 502


# ==========================================
# ACTIVITY 9 - IMPORT STUDENT
# ==========================================

@app.route("/import-student", methods=["POST"])
def import_student():
    data = request.get_json(silent=True)

    if not data:
        return jsonify({"error": "JSON data is required"}), 400

    required_fields = [
        "student_id", "name", "program", "year", "section"
    ]

    for field in required_fields:
        if field not in data or str(data[field]).strip() == "":
            return jsonify({"error": f"{field} is required"}), 400

    try:
        year = int(data["year"])
    except (ValueError, TypeError):
        return jsonify({"error": "Year must be a number"}), 400

    try:
        with get_db_connection() as conn:
            cursor = conn.execute(
                """
                INSERT INTO students
                (student_id, name, program, year, section, source)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    data["student_id"],
                    data["name"],
                    data["program"],
                    year,
                    data["section"],
                    "Classmate API"
                )
            )

            new_id = cursor.lastrowid

        return jsonify({
            "message": "Student imported successfully",
            "id": new_id,
            "source": "Classmate API"
        }), 201

    except sqlite3.IntegrityError:
        return jsonify({
            "error": "Student record already exists in your database"
        }), 409

    except sqlite3.Error:
        app.logger.exception("Could not import student")
        return jsonify({"error": "Database import failed"}), 500


# ==========================================
# ACTIVITY 9 - SEND RECORD TO CLASSMATE API
# ==========================================

@app.route("/send-to-partner", methods=["POST"])
def send_to_partner():
    data = request.get_json(silent=True)

    if not data:
        return jsonify({"error": "JSON data is required"}), 400

    required_fields = [
        "student_id", "name", "program", "year", "section"
    ]

    for field in required_fields:
        if field not in data or str(data[field]).strip() == "":
            return jsonify({"error": f"{field} is required"}), 400

    try:
        year = int(data["year"])
    except (ValueError, TypeError):
        return jsonify({"error": "Year must be a number"}), 400

    payload = {
        "student_id": data["student_id"],
        "name": data["name"],
        "program": data["program"],
        "year": year,
        "section": data["section"],
        "source": "Partner API"
    }

    try:
        response = requests.post(
            CLASSMATE_API_URL,
            json=payload,
            timeout=15
        )

        try:
            result = response.json()
        except ValueError:
            result = {"message": response.text}

        return jsonify({
            "message": "Response received from classmate API",
            "partner_status": response.status_code,
            "partner_response": result
        }), response.status_code

    except requests.RequestException as error:
        app.logger.exception("Could not send record to classmate API")
        return jsonify({
            "error": "Unable to send record to classmate API",
            "details": str(error)
        }), 502


# ==========================================
# RUN APPLICATION
# ==========================================

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )
