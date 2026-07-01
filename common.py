import os
import sqlite3
import pandas as pd
import pickle

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
    if not os.path.exists(MODEL_PATH):
        raise FileNotFoundError(f"Model file not found: {MODEL_PATH}")
    # Try joblib at call time so missing joblib doesn't break module import
    try:
        import joblib
    except Exception:
        joblib = None

    if joblib is not None:
        try:
            return joblib.load(MODEL_PATH)
        except Exception:
            pass

    # fallback to pickle.load
    with open(MODEL_PATH, "rb") as f:
        return pickle.load(f)


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


def ensure_database_has_students(cursor, target_count=200):
    cursor.execute("SELECT COUNT(*) FROM students")
    current_count = cursor.fetchone()[0]
    if current_count >= target_count:
        return

    if not os.path.exists(STUDENT_DATA_PATH):
        return

    data = pd.read_csv(STUDENT_DATA_PATH)
    if data.empty:
        return

    next_index = current_count + 1
    rows_to_add = min(target_count - current_count, len(data))
    for idx, row in data.iloc[:rows_to_add].iterrows():
        student_number = next_index + idx
        name = f"Student {student_number:03d}"
        student_id = f"S{student_number:04d}"
        attendance = float(row["Attendance"])
        study_hours = float(row["StudyHours"])
        previous_marks = float(row["PreviousMarks"])
        predicted_marks = float(row["FinalMarks"])
        risk = "Low" if predicted_marks >= 70 else ("Medium" if predicted_marks >= 50 else "High")
        cursor.execute(
            "INSERT INTO students (name, student_id, attendance, study_hours, previous_marks, predicted_marks, risk) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (name, student_id, attendance, study_hours, previous_marks, predicted_marks, risk),
        )
    cursor.connection.commit()
