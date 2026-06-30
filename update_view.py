import pandas as pd
import streamlit as st


def render_update(cursor, model):
    st.subheader("✏️ Update Student")
    update_id = st.text_input("Enter Student ID to Update", key="update_student_id")
    new_attendance = st.number_input("New Attendance", 0, 100, key="new_attendance")
    new_study_hours = st.number_input("New Study Hours", 0, 15, key="new_study_hours")
    new_previous_marks = st.number_input("New Previous Marks", 0, 100, key="new_previous_marks")

    if st.button("Update Student", key="update_student_button"):
        if update_id.strip():
            input_df = pd.DataFrame(
                [
                    {
                        "Attendance": new_attendance,
                        "StudyHours": new_study_hours,
                        "PreviousMarks": new_previous_marks,
                    }
                ]
            )
            new_prediction = float(model.predict(input_df)[0])

            if new_prediction >= 70:
                new_risk = "Low"
            elif new_prediction >= 50:
                new_risk = "Medium"
            else:
                new_risk = "High"

            cursor.execute(
                """
                UPDATE students
                SET attendance=?, study_hours=?, previous_marks=?, predicted_marks=?, risk=?
                WHERE student_id=?
                """,
                (
                    new_attendance,
                    new_study_hours,
                    new_previous_marks,
                    round(new_prediction, 2),
                    new_risk,
                    update_id,
                ),
            )
            cursor.connection.commit()

            if cursor.rowcount > 0:
                st.success("Student updated successfully")
            else:
                st.warning("No student found with that ID")
        else:
            st.error("Please enter a student ID")
