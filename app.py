
import sqlite3
from pathlib import Path
from flask import Flask, jsonify, request, render_template

app = Flask(__name__)

# Use the database file in the project directory
BASE_DIR = Path(__file__).resolve().parent
DATABASE = BASE_DIR / "students.db"


def get_db_connection():
    conn = sqlite3.connect(str(DATABASE))
    conn.row_factory = sqlite3.Row
    return conn


# Home page
@app.route("/")
def home():
    return render_template("index.html")


# Student profile API
@app.route("/student")
def get_student():
    return jsonify({
        "student_id": "24-00228",
        "name": "Josil Paclibar",
        "program": "BSIT",
        "year": 3,
        "section": "Dijkstra"
    })


# Greeting API: /hello?name=Josil
@app.route("/hello")
def say_hello():
    name = request.args.get("name", "Student")
    return jsonify({"message": f"Hello, {name}!"})


# Course information API
@app.route("/course")
def get_course():
    return jsonify({
        "course_code": "IT 3120",
        "course_title": "Information Technology",
        "instructor": "Rene Ardou",
        "semester": "First Semester",
        "academic_year": "2026-2027"
    })


# Get all students
@app.route("/students")
def get_students():
    conn = get_db_connection()
    try:
        students = conn.execute(
            "SELECT * FROM students ORDER BY id"
        ).fetchall()
        return jsonify([dict(student) for student in students])
    except sqlite3.Error as error:
        app.logger.exception("Could not retrieve students")
        return jsonify({"error": "Database query failed"}), 500
    finally:
        conn.close()


# Get one student by database ID
@app.route("/students/<int:id>")
def get_student_by_id(id):
    conn = get_db_connection()
    try:
        student = conn.execute(
            "SELECT * FROM students WHERE id = ?",
            (id,)
        ).fetchone()

        if student is None:
            return jsonify({"error": "Student not found"}), 404

        return jsonify(dict(student))
    except sqlite3.Error:
        app.logger.exception("Could not retrieve student")
        return jsonify({"error": "Database query failed"}), 500
    finally:
        conn.close()


# Get students by section
@app.route("/students/section/<section>")
def get_students_by_section(section):
    conn = get_db_connection()
    try:
        students = conn.execute(
            "SELECT * FROM students WHERE section = ? ORDER BY id",
            (section,)
        ).fetchall()
        return jsonify([dict(student) for student in students])
    except sqlite3.Error:
        app.logger.exception("Could not filter students by section")
        return jsonify({"error": "Database query failed"}), 500
    finally:
        conn.close()


# Get students by program
@app.route("/students/program/<program>")
def get_students_by_program(program):
    conn = get_db_connection()
    try:
        students = conn.execute(
            "SELECT * FROM students WHERE program = ? ORDER BY id",
            (program,)
        ).fetchall()
        return jsonify([dict(student) for student in students])
    except sqlite3.Error:
        app.logger.exception("Could not filter students by program")
        return jsonify({"error": "Database query failed"}), 500
    finally:
        conn.close()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
