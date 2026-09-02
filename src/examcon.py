import webbrowser
import sqlite3
from pathlib import Path
from config import get_user_data_dir

EXAMCON_URL = "https://examcon.uiu.ac.bd/"
DB_PATH = get_user_data_dir() / "student_records.db"


def open_examcon_portal():
    """Opens official UIU Exam Controller portal in the default web browser."""
    webbrowser.open(EXAMCON_URL)


def init_exam_schedule_table():
    """Creates local storage table for caching exam dates, rooms, and seat details."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS exam_schedules (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            course_code TEXT NOT NULL,
            exam_type TEXT NOT NULL,
            exam_date TEXT NOT NULL,
            exam_time TEXT NOT NULL,
            room_no TEXT,
            recorded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()


def save_exam_entry(course_code: str, exam_type: str, exam_date: str, exam_time: str, room_no: str):
    init_exam_schedule_table()
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO exam_schedules (course_code, exam_type, exam_date, exam_time, room_no)
        VALUES (?, ?, ?, ?, ?)
    """, (course_code.strip().upper(), exam_type.strip(), exam_date.strip(), exam_time.strip(), room_no.strip().upper()))
    conn.commit()
    conn.close()


def get_all_exam_entries():
    init_exam_schedule_table()
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT id, course_code, exam_type, exam_date, exam_time, room_no FROM exam_schedules ORDER BY exam_date ASC")
    rows = cursor.fetchall()
    conn.close()
    return [{
        "id": r[0],
        "course_code": r[1],
        "exam_type": r[2],
        "exam_date": r[3],
        "exam_time": r[4],
        "room_no": r[5] or "TBA"
    } for r in rows]


def delete_exam_entry(entry_id: int):
    init_exam_schedule_table()
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM exam_schedules WHERE id = ?", (entry_id,))
    conn.commit()
    conn.close()
