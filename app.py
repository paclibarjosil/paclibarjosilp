
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

# Set your classmate's API URL in the environment.
CLASSMATE_API_URL = os.environ.get(
    "CLASSMATE_API_URL",
    ""
)


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


# ==========================================
# GREETING API
# ==========================================

@app.route("/hello")
def say_hello():
    name = request.args.get("name", "Student")
    return jsonify({
        "message": f"Hello, {name}!"
    })


# ==========================================
# COURSE API
# ==========================================

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
# ACTIVITY 7 - GET ALL STUDENTS
# ==========================================

@app.route("/students", methods=["GET"])
def get_students():
    try:
        conn = get_db_connection()
        students = conn.execute(
            "SELECT * FROM students"
        ).fetchall()
        conn.close()

        return jsonify([dict(student) for student in students])

    except sqlite3.Error:
        app.logger.exception("Could not retrieve students")
        return jsonify({"error": "Database query failed"}), 500


# ==========================================
# ACTIVITY 7 - GET ONE STUDENT
# ==========================================

@app.route("/students/<int:id>", methods=["GET"])
def get_student_by_id(id):
    try:
        conn = get_db_connection()
        student = conn.execute(
            "SELECT * FROM students WHERE id = ?",
            (id,)
        ).fetchone()
        conn.close()

        if student is None:
            return jsonify({"error": "Student not found"}), 404

        return jsonify(dict(student))

    except sqlite3.Error:
        app.logger.exception("Could not retrieve student")
        return jsonify({"error": "Database query failed"}), 500


# ==========================================
# ACTIVITY 7 - FILTER STUDENTS BY SECTION
# ==========================================

@app.route("/students/section/<section>", methods=["GET"])
def get_students_by_section(section):
    try:
        conn = get_db_connection()
        students = conn.execute(
            "SELECT * FROM students WHERE section = ?",
            (section,)
        ).fetchall()
        conn.close()

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
        conn = get_db_connection()
        students = conn.execute(
            "SELECT * FROM students"
        ).fetchall()
        conn.close()

        return jsonify([dict(student) for student in students])

    except sqlite3.Error:
        app.logger.exception("Could not retrieve API students")
        return jsonify({"error": "Database query failed"}), 500


# ==========================================
# ACTIVITY 8 - ADD STUDENT
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
            return jsonify({
                "error": f"{field} is required"
            }), 400

    try:
        year = int(data["year"])
    except (ValueError, TypeError):
        return jsonify({"error": "Year must be a number"}), 400

    try:
        conn = get_db_connection()

        conn.execute(
            """
            INSERT INTO students
            (student_id, name, program, year, section)
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                data["student_id"],
                data["name"],
                data["program"],
                year,
                data["section"]
            )
        )

        conn.commit()
        new_id = conn.execute(
            "SELECT last_insert_rowid()"
        ).fetchone()[0]
        conn.close()

        return jsonify({
            "message": "Student added successfully",
            "id": new_id
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
        conn = get_db_connection()
        student = conn.execute(
            "SELECT * FROM students WHERE id = ?",
            (id,)
        ).fetchone()
        conn.close()

        if student is None:
            return jsonify({"error": "Student not found"}), 404

        return jsonify(dict(student))

    except sqlite3.Error:
        app.logger.exception("Could not retrieve student")
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
        "student_id", "name", "program", "year", "section"
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
        conn = get_db_connection()

        student = conn.execute(
            "SELECT id FROM students WHERE id = ?",
            (id,)
        ).fetchone()

        if student is None:
            conn.close()
            return jsonify({"error": "Student not found"}), 404

        set_clause = ", ".join(
            f"{field} = ?" for field in updates
        )

        values = list(updates.values()) + [id]

        conn.execute(
            f"UPDATE students SET {set_clause} WHERE id = ?",
            values
        )

        conn.commit()
        conn.close()

        return jsonify({
            "message": "Student updated successfully"
        })

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
        conn = get_db_connection()

        result = conn.execute(
            "DELETE FROM students WHERE id = ?",
            (id,)
        )

        conn.commit()
        deleted = result.rowcount
        conn.close()

        if deleted == 0:
            return jsonify({"error": "Student not found"}), 404

        return jsonify({
            "message": "Student deleted successfully"
        })

    except sqlite3.Error:
        app.logger.exception("Could not delete student")
        return jsonify({"error": "Database delete failed"}), 500


# ==========================================
# CLASSMATE API - RETRIEVE EXTERNAL RECORDS
# ==========================================

@app.route("/api/classmates", methods=["GET"])
def get_classmate_records():
    if not CLASSMATE_API_URL:
        return jsonify({
            "error": "Classmate API URL is not configured"
        }), 503

    try:
        response = requests.get(
            CLASSMATE_API_URL,
            timeout=10
        )

        response.raise_for_status()

        return jsonify(response.json()), response.status_code

    except requests.RequestException:
        app.logger.exception("Could not retrieve classmate records")
        return jsonify({
            "error": "Unable to retrieve classmate records"
        }), 502

    except ValueError:
        return jsonify({
            "error": "Classmate API returned invalid JSON"
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
