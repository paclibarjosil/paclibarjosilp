import sqlite3
from flask import Flask, jsonify, request, render_template

app = Flask(__name__)

# SQLite Database Connection
def get_db_connection():
    conn = sqlite3.connect("students.db")
    conn.row_factory = sqlite3.Row
    return conn


# Home Page - Web Interface
@app.route("/")
def home():
    return render_template("index.html")


# Existing Student Information API
@app.route("/student")
def get_student():
    return jsonify({
        "student_id": "24-00228",
        "name": "Josil Paclibar",
        "program": "BSIT",
        "year": 3,
        "section": "Dijkstra"
    })


# Greeting API
@app.route("/hello")
def say_hello():
    name = request.args.get("name", "Student")

    return jsonify({
        "message": f"Hello, {name}!"
    })


# Existing Course Information API
@app.route("/course")
def get_course():
    return jsonify({
        "course_code": "IT 3120",
        "course_title": "Information Technology",
        "instructor": "Rene Ardou",
        "semester": "First Semester",
        "academic_year": "2026-2027"
    })


# Activity 7 - Get All Students from SQLite
@app.route("/students")
def get_students():
    conn = get_db_connection()

    students = conn.execute(
        "SELECT * FROM students"
    ).fetchall()

    conn.close()

    return jsonify([dict(student) for student in students])


# Activity 7 - Get One Student by Database ID
@app.route("/students/<int:id>")
def get_student_by_id(id):
    conn = get_db_connection()

    student = conn.execute(
        "SELECT * FROM students WHERE id = ?",
        (id,)
    ).fetchone()

    conn.close()

    if student is None:
        return jsonify({
            "error": "Student not found"
        }), 404

    return jsonify(dict(student))


# Additional Task - Get Students by Section
@app.route("/students/section/<section>")
def get_students_by_section(section):
    conn = get_db_connection()

    students = conn.execute(
        "SELECT * FROM students WHERE section = ?",
        (section,)
    ).fetchall()

    conn.close()

    return jsonify([dict(student) for student in students])


# Run Flask Application
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
