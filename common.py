import os
import sqlite3
import pandas as pd
import joblib

DB_PATH = "students.db"
MODEL_PATH = "model.pkl"
STUDENT_DATA_PATH = "student_data.csv"
HISTORY_PATH = "history.csv"


def init_db():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS students(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            student_id TEXT,
            attendance REAL,
            study_hours REAL,
            previous_marks REAL,
            predicted_marks REAL,
            risk TEXT
        )
        """
    )
    conn.commit()
    return conn, cursor


def load_model():
    return joblib.load(MODEL_PATH)


def get_dashboard_dataframe(cursor):
    cursor.execute("SELECT * FROM students")
    rows = cursor.fetchall()
    return pd.DataFrame(
        rows,
        columns=[
            "ID",
            "Name",
            "Student ID",
            "Attendance",
            "Study Hours",
            "Previous Marks",
            "Predicted Marks",
            "Risk",
        ],
    )


def get_history_dataframe():
    if os.path.exists(HISTORY_PATH):
        return pd.read_csv(HISTORY_PATH)
    return pd.DataFrame(columns=["Name", "ID", "Attendance", "Study Hours", "Previous Marks", "Predicted Marks"])


def save_history_entry(history_entry):
    history_df = pd.DataFrame([history_entry])
    if os.path.exists(HISTORY_PATH):
        history_df.to_csv(HISTORY_PATH, mode="a", header=False, index=False)
    else:
        history_df.to_csv(HISTORY_PATH, index=False)
