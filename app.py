
from flask import Flask, jsonify, request

app = Flask(__name__)


# Home page
@app.route("/")
def home():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>My First Flask API</title>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <style>
            body {
                font-family: Arial, sans-serif;
                background: #f4f6f9;
                margin: 0;
                padding: 30px 15px;
            }
            .container {
                max-width: 600px;
                margin: auto;
                background: white;
                padding: 25px;
                border-radius: 12px;
                box-shadow: 0 3px 12px #0002;
            }
            h1 { color: #1769aa; }
            h2 { color: #333; }
            a {
                display: block;
                background: #1769aa;
                color: white;
                padding: 12px;
                margin-top: 12px;
                text-decoration: none;
                border-radius: 6px;
                text-align: center;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Welcome to My First API!</h1>
            <h2>Student Information</h2>
            <p><b>Name:</b> Josil Paclibar</p>
            <p><b>Course:</b> BSIT</p>
            <p><b>Section:</b> BSIT 3B</p>
            <p><b>Subject:</b> IT 3120</p>
            <hr>
            <p>Flask API is running successfully!</p>
            <a href="/student">View Student API</a>
            <a href="/hello?name=Josil%20Paclibar">Test Hello API</a>
        </div>
    </body>
    </html>
    """


# Student information API
@app.route("/student")
def student():
    return jsonify({
        "name": "Josil Paclibar",
        "program": "BSIT",
        "year": 3,
        "section": "BSIT 3B"
    })


# Hello API with a query parameter
@app.route("/hello")
def hello():
    name = request.args.get("name", "Student")
    return jsonify({
        "message": f"Hello, {name}!"
    })


# Course information API
@app.route("/course")
def course():
    return jsonify({
        "course_code": "IT 3120",
        "course_title": "Information Technology",
        "instructor": "Rene Ardou"
    })


if __name__ == "__main__":
    app.run(debug=False)
