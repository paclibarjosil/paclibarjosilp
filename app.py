
from flask import Flask, jsonify, request, render_template

app = Flask(__name__)


# Home page - Web Interface
@app.route('/')
def home():
    return render_template('index.html')


# Student Information API
@app.route('/student')
def get_student():
    return jsonify({
        "student_id": "24-00228",
        "name": "Josil Paclibar",
        "program": "BSIT",
        "year": 3,
        "section": "Dijkstra"
    })


# Greeting API
@app.route('/hello')
def say_hello():
    name = request.args.get('name', 'Student')

    return jsonify({
        "message": f"Hello, {name}!"
    })


# Custom API Endpoint - Course Information
@app.route('/course')
def get_course():
    return jsonify({
        "course_code": "IT 3120",
        "course_title": "Information Technology",
        "instructor": "Rene Ardou",
        "semester": "First Semester",
        "academic_year": "2026-2027"
    })


# Run Flask Application
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
