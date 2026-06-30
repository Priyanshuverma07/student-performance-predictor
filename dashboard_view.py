import pandas as pd
import streamlit as st
from datetime import datetime

from common import STUDENT_DATA_PATH, get_history_dataframe


def render_dashboard(dashboard):
    st.header("📊 Analytics Dashboard")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Students", len(dashboard))
    with col2:
        st.metric("Low Risk", len(dashboard[dashboard["Risk"] == "Low"]))
    with col3:
        st.metric("Medium Risk", len(dashboard[dashboard["Risk"] == "Medium"]))
    with col4:
        st.metric("High Risk", len(dashboard[dashboard["Risk"] == "High"]))

    avg_predicted_marks = round(dashboard["Predicted Marks"].mean(), 2) if not dashboard.empty else 0
    st.metric("Average Predicted Marks", avg_predicted_marks)

    if not dashboard.empty:
        top_student = dashboard.loc[dashboard["Predicted Marks"].idxmax()]
        st.success("🏆 Top Performer")
        st.write("Name :", top_student["Name"])
        st.write("Predicted Marks :", top_student["Predicted Marks"])

        low_student = dashboard.loc[dashboard["Predicted Marks"].idxmin()]
        st.error("📉 Lowest Performer")
        st.write("Name :", low_student["Name"])
        st.write("Predicted Marks :", low_student["Predicted Marks"])
    else:
        st.info("No student data available yet. Add a prediction to see top and lowest performers.")

    st.markdown("---")
    data = pd.read_csv(STUDENT_DATA_PATH)

    st.subheader("📈 Analytics Charts")
    chart_col1, chart_col2 = st.columns(2)

    with chart_col1:
        st.write("Attendance Distribution")
        st.bar_chart(data["Attendance"])

    with chart_col2:
        st.write("Final Marks Trend")
        st.line_chart(data["FinalMarks"])

    st.markdown("---")

    if not dashboard.empty:
        risk_counts = dashboard["Risk"].value_counts().reindex(["Low", "Medium", "High"], fill_value=0)
        st.write("Risk Level Distribution")
        st.bar_chart(risk_counts)

    history = get_history_dataframe()
    if not history.empty:
        st.subheader("Prediction History")
        st.dataframe(history)
