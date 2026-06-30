import pandas as pd
import streamlit as st


def render_bulk(model):
    st.header("Bulk Student Prediction")
    st.info("Please upload a .csv file with Attendance, StudyHours, and PreviousMarks columns.")
    uploaded_file = st.file_uploader("Upload Student CSV file", key="bulk_upload")

    if uploaded_file is not None:
        if not uploaded_file.name.lower().endswith(".csv"):
            st.error("Please upload a valid .csv file.")
            return

        students = pd.read_csv(uploaded_file)
        st.write("Uploaded Data")
        st.dataframe(students)

        required_columns = ["Attendance", "StudyHours", "PreviousMarks"]
        if all(column in students.columns for column in required_columns):
            students["Predicted Marks"] = model.predict(students[required_columns])

            risk = []
            for marks in students["Predicted Marks"]:
                if marks >= 70:
                    risk.append("Low")
                elif marks >= 50:
                    risk.append("Medium")
                else:
                    risk.append("High")

            students["Risk Level"] = risk
            st.subheader("Prediction Result")
            st.dataframe(students)
        else:
            st.error("Uploaded CSV must contain Attendance, StudyHours, and PreviousMarks columns.")
