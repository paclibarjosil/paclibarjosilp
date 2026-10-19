import sqlite3

conn = sqlite3.connect("students.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id TEXT NOT NULL,
    name TEXT NOT NULL,
    program TEXT NOT NULL,
    year INTEGER NOT NULL,
    section TEXT NOT NULL
)
""")

# Reset sample records whenever this script runs
cursor.execute("DELETE FROM students")

students = [
    ("2026-00123", "John Michael Pabilona", "BSIT", 3, "B"),
    ("2026-00124", "Stephen Jeck Paclibar", "BSIT", 3, "B"),
    ("2026-00125", "Harold Redolosa Padernal", "BSIT", 3, "B"),
    ("2026-00126", "Keven Olesco", "BSIT", 3, "B"),
    ("2026-00127", "Grant David", "BSIT", 3, "B")
]

cursor.executemany("""
INSERT INTO students (student_id, name, program, year, section)
VALUES (?, ?, ?, ?, ?)
""", students)

conn.commit()
conn.close()

print("Database created successfully.")
