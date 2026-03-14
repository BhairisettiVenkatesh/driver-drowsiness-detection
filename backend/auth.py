import sqlite3
import os
from fastapi import APIRouter
from fastapi import HTTPException

router = APIRouter()


# absolute database path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "database", "users.db")


# connect database safely
conn = sqlite3.connect(DB_PATH, check_same_thread=False)
cursor = conn.cursor()


# create users table
cursor.execute("""
CREATE TABLE IF NOT EXISTS users(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
)
""")

conn.commit()


# create events table (for logging detection results)
cursor.execute("""
CREATE TABLE IF NOT EXISTS events(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT,
    ear REAL,
    mar REAL,
    head_angle REAL,
    fatigue_score REAL,
    status TEXT
)
""")

conn.commit()


# REGISTER USER
@router.post("/register")
def register(user: dict):

    username = user.get("username")
    password = user.get("password")

    # validation
    if not username or not password:

        raise HTTPException(
            status_code=400,
            detail="Username and password required"
        )

    try:

        cursor.execute(
            "INSERT INTO users(username,password) VALUES (?,?)",
            (username, password)
        )

        conn.commit()

        return {
            "status": "success",
            "message": "User registered successfully"
        }

    except sqlite3.IntegrityError:

        return {
            "status": "exists",
            "message": "User already exists"
        }



# LOGIN USER
@router.post("/login")
def login(user: dict):

    username = user.get("username")
    password = user.get("password")

    if not username or not password:

        raise HTTPException(
            status_code=400,
            detail="Username and password required"
        )

    cursor.execute(
        "SELECT * FROM users WHERE username=? AND password=?",
        (username, password)
    )

    result = cursor.fetchone()

    if result:

        return {
            "status": "success",
            "message": "Login successful"
        }

    return {
        "status": "invalid",
        "message": "Invalid username or password"
    }