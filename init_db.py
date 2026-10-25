
import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DATABASE = BASE_DIR / "students.db"


def initialize_database():
    conn = sqlite3.connect(str(DATABASE))

    try:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS students (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id TEXT NOT NULL UNIQUE,
                name TEXT NOT NULL,
                program TEXT NOT NULL,
                year INTEGER NOT NULL,
                section TEXT NOT NULL
            )
        """)

        count = conn.execute(
            "SELECT COUNT(*) FROM students"
        ).fetchone()[0]

        if count == 0:
            sample_students = [
                ("2026-00123", "John Michael Pabilona", "BSIT", 3, "B"),
                ("2026-00124", "Stephen Jeck Paclibar", "BSIT", 3, "B"),
                ("2026-00125", "Harold Redolosa Padernal", "BSIT", 3, "B"),
                ("2026-00126", "Keven Olesco", "BSIT", 3, "B"),
                ("2026-00127", "Grant David", "BSIT", 3, "B")
            ]

            conn.executemany("""
                INSERT INTO students
                (student_id, name, program, year, section)
                VALUES (?, ?, ?, ?, ?)
            """, sample_students)

        conn.commit()
        print(f"Database initialized: {DATABASE}")

    finally:
        conn.close()


if __name__ == "__main__":
    initialize_database()
