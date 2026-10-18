@app.route("/")
def home():
    return """
    <html>
    <head>
        <title>My First Flask API</title>
    </head>
    <body>
        <h1>Welcome to My First API!</h1>
        <h2>Student Information</h2>
        <p>Name: Josil Paclibar</p>
        <p>Course: BSIT</p>
        <p>Section: BSIT 3B</p>
        <p>Subject: IT 3120</p>
        <hr>
        <p>Flask API is running successfully!</p>
        <a href="/student">View Student API</a><br>
        <a href="/hello?name=Josil%20Paclibar">Test Hello API</a>
    </body>
    </html>
    """
