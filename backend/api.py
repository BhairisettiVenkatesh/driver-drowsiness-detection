from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import threading
import sqlite3

from backend.auth import router
from backend import realtime

# =========================
# CREATE FASTAPI APP
# =========================

app = FastAPI()

# =========================
# ENABLE CORS FOR FRONTEND
# =========================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =========================
# INCLUDE AUTH ROUTES
# =========================

app.include_router(router)

# =========================
# TEST ROUTE
# =========================

@app.get("/")
def home():

    return {"message": "Backend running successfully"}


# =========================
# DETECTION CONTROL VARIABLES
# =========================

detection_thread = None
detection_running = False


# =========================
# START DETECTION ENDPOINT
# =========================

@app.get("/start-detection")
def start_detection():

    global detection_thread
    global detection_running

    if detection_running:

        return {"status": "already running"}

    try:

        detection_running = True

        detection_thread = threading.Thread(
            target=realtime.start_detection,
            daemon=True
        )

        detection_thread.start()

        print("Detection thread started")

        return {"status": "started"}

    except Exception as e:

        detection_running = False

        print("Error starting detection:", e)

        return {"status": "error", "message": str(e)}



# =========================
# STOP DETECTION ENDPOINT
# =========================

@app.get("/stop-detection")
def stop_detection():

    global detection_running
    global detection_thread

    if not detection_running:

        return {"status": "not running"}

    try:

        realtime.stop_detection()

        detection_running = False
        detection_thread = None

        print("Detection stopped")

        return {"status": "stopped"}

    except Exception as e:

        print("Error stopping detection:", e)

        return {"status": "error", "message": str(e)}


# =========================
#  NEW ANALYTICS API
# =========================

@app.get("/analytics")
def analytics():

    conn = sqlite3.connect("database/users.db")
    cursor = conn.cursor()

    cursor.execute("""
    SELECT status, COUNT(*)
    FROM detection_logs
    GROUP BY status
    """)

    data = cursor.fetchall()

    conn.close()

    return {"data": data}