import sqlite3
from pathlib import Path
from config import get_user_data_dir

DB_PATH = get_user_data_dir() / "student_records.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS trimesters (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            trimester_name TEXT NOT NULL,
            gpa REAL NOT NULL,
            credits REAL NOT NULL,
            recorded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

def add_trimester_record(name: str, gpa: float, credits: float):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO trimesters (trimester_name, gpa, credits)
        VALUES (?, ?, ?)
    """, (name, gpa, credits))
    conn.commit()
    conn.close()

def get_all_trimesters():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT id, trimester_name, gpa, credits FROM trimesters ORDER BY id ASC")
    rows = cursor.fetchall()
    conn.close()
    return [{"id": r[0], "name": r[1], "gpa": r[2], "credits": r[3]} for r in rows]

def get_cumulative_metrics():
    records = get_all_trimesters()
    if not records:
        return {"cgpa": 0.0, "total_credits": 0.0}

    total_credits = sum(r["credits"] for r in records)
    if total_credits == 0:
        return {"cgpa": 0.0, "total_credits": 0.0}

    total_points = sum(r["gpa"] * r["credits"] for r in records)
    cgpa = total_points / total_credits
    return {"cgpa": round(cgpa, 2), "total_credits": round(total_credits, 1)}

def delete_trimester_record(record_id: int):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM trimesters WHERE id = ?", (record_id,))
    conn.commit()
    conn.close()
