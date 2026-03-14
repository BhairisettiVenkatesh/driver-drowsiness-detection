import sqlite3
import os
from datetime import datetime

# get absolute path of database
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "database", "users.db")


def log_event(user, ear, mar, head, score, level):

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # create detection_logs table if not exists
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS detection_logs(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        timestamp TEXT,
        ear REAL,
        mar REAL,
        head_angle REAL,
        fatigue_score REAL,
        status TEXT
    )
    """)

    # insert detection event
    cursor.execute("""
    INSERT INTO detection_logs
    (username,timestamp,ear,mar,head_angle,fatigue_score,status)
    VALUES(?,?,?,?,?,?,?)
    """,(
        user,
        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        float(ear),
        float(mar),
        float(head),
        float(score),
        level
    ))

    conn.commit()
    conn.close()