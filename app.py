
import sqlite3
from flask import Flask, jsonify, request, render_template

app = Flask(__name__)

# ==========================================
# DATABASE CONNECTION
# ==========================================

def get_db_connection():
    conn = sqlite3.connect("students.db")
    conn.row_factory = sqlite3.Row
    return conn


# ==========================================
# HOME PAGE
# ==========================================

@app.route("/")
def home():
    return render_template("index.html")


# ==========================================
# EXISTING STUDENT INFORMATION API
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
# EXISTING COURSE INFORMATION API
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
    conn = get_db_connection()

    students = conn.execute(
        "SELECT * FROM students ORDER BY id"
    ).fetchall()

    conn.close()

    return jsonify([dict(student) for student in students])


# ==========================================
# ACTIVITY 7 - GET ONE STUDENT BY ID
# ==========================================

@app.route("/students/<int:id>", methods=["GET"])
def get_student_by_id(id):
    conn = get_db_connection()

    student = conn.execute(
        "SELECT * FROM students WHERE id = ?",
        (id,)
    ).fetchone()

    conn.close()

    if student is None:
        return jsonify({"error": "Student not found"}), 404

    return jsonify(dict(student))


# ==========================================
# ACTIVITY 7 - GET STUDENTS BY SECTION
# ==========================================

@app.route("/students/section/<section>", methods=["GET"])
def get_students_by_section(section):
    conn = get_db_connection()

    students = conn.execute(
        "SELECT * FROM students WHERE section = ?",
        (section,)
    ).fetchall()

    conn.close()

    return jsonify([dict(student) for student in students])


# ==========================================
# ACTIVITY 8 - READ ALL STUDENTS
# GET /api/students
# ==========================================

@app.route("/api/students", methods=["GET"])
def api_students():
    conn = get_db_connection()

    students = conn.execute(
        "SELECT * FROM students ORDER BY id"
    ).fetchall()

    conn.close()

    return jsonify([dict(student) for student in students])


# ==========================================
# ACTIVITY 8 - CREATE STUDENT
# POST /api/students
# ==========================================

@app.route("/api/students", methods=["POST"])
def add_student():
    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({"error": "Valid JSON data is required"}), 400

    required_fields = [
        "student_id", "name", "program", "year", "section"
    ]

    for field in required_fields:
        if field not in data or str(data[field]).strip() == "":
            return jsonify({
                "error": f"Missing required field: {field}"
            }), 400

    try:
        year = int(data["year"])
    except (ValueError, TypeError):
        return jsonify({"error": "Year must be a number"}), 400

    conn = get_db_connection()

    try:
        cursor = conn.execute(
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
        new_id = cursor.lastrowid

    except sqlite3.Error as error:
        conn.rollback()
        return jsonify({"error": str(error)}), 500

    finally:
        conn.close()

    return jsonify({
        "message": "Student added successfully",
        "id": new_id
    }), 201


# ==========================================
# ACTIVITY 8 - READ ONE STUDENT
# GET /api/students/<id>
# ==========================================

@app.route("/api/students/<int:id>", methods=["GET"])
def api_get_student(id):
    conn = get_db_connection()

    student = conn.execute(
        "SELECT * FROM students WHERE id = ?",
        (id,)
    ).fetchone()

    conn.close()

    if student is None:
        return jsonify({"error": "Student not found"}), 404

    return jsonify(dict(student))


# ==========================================
# ACTIVITY 8 - UPDATE STUDENT
# PUT /api/students/<id>
# ==========================================

@app.route("/api/students/<int:id>", methods=["PUT"])
def update_student(id):
    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({"error": "Valid JSON data is required"}), 400

    required_fields = [
        "student_id", "name", "program", "year", "section"
    ]

    for field in required_fields:
        if field not in data or str(data[field]).strip() == "":
            return jsonify({
                "error": f"Missing required field: {field}"
            }), 400

    try:
        year = int(data["year"])
    except (ValueError, TypeError):
        return jsonify({"error": "Year must be a number"}), 400

    conn = get_db_connection()

    try:
        existing = conn.execute(
            "SELECT id FROM students WHERE id = ?",
            (id,)
        ).fetchone()

        if existing is None:
            return jsonify({"error": "Student not found"}), 404

        conn.execute(
            """
            UPDATE students
            SET student_id = ?,
                name = ?,
                program = ?,
                year = ?,
                section = ?
            WHERE id = ?
            """,
            (
                data["student_id"],
                data["name"],
                data["program"],
                year,
                data["section"],
                id
            )
        )

        conn.commit()

    except sqlite3.Error as error:
        conn.rollback()
        return jsonify({"error": str(error)}), 500

    finally:
        conn.close()

    return jsonify({
        "message": "Student updated successfully",
        "id": id
    })


# ==========================================
# ACTIVITY 8 - DELETE STUDENT
# DELETE /api/students/<id>
# ==========================================

@app.route("/api/students/<int:id>", methods=["DELETE"])
def delete_student(id):
    conn = get_db_connection()

    try:
        cursor = conn.execute(
            "DELETE FROM students WHERE id = ?",
            (id,)
        )

        conn.commit()
        deleted = cursor.rowcount

    except sqlite3.Error as error:
        conn.rollback()
        return jsonify({"error": str(error)}), 500

    finally:
        conn.close()

    if deleted == 0:
        return jsonify({"error": "Student not found"}), 404

    return jsonify({
        "message": "Student deleted successfully",
        "id": id
    })


# ==========================================
# RUN FLASK APPLICATION
# ==========================================

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )
