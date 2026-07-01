import io
import os
import pandas as pd
import streamlit as st
from datetime import datetime
_HAS_REPORTLAB = True
try:
    from reportlab.lib import colors
    from reportlab.lib.enums import TA_CENTER
    from reportlab.lib.pagesizes import letter
    from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
    from reportlab.lib.units import inch
    from reportlab.platypus import Image, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle
    from reportlab.graphics.shapes import Drawing, Rect, String, Circle
    from reportlab.graphics.charts.piecharts import Pie
    from reportlab.graphics.charts.lineplots import LinePlot
    from reportlab.graphics.barcode import qr
except Exception:
    _HAS_REPORTLAB = False

from common import save_history_entry


def generate_pdf_report(student_info):
    if not _HAS_REPORTLAB:
        raise RuntimeError("PDF generation requires the 'reportlab' package. Install it or remove PDF download.")

    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        rightMargin=40,
        leftMargin=40,
        topMargin=60,
        bottomMargin=40,
    )

    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        name="Title",
        parent=styles["Heading1"],
        alignment=TA_CENTER,
        fontSize=24,
        textColor=colors.HexColor("#0b3d91"),
        spaceAfter=14,
    )
    subtitle_style = ParagraphStyle(
        name="Subtitle",
        parent=styles["Heading2"],
        alignment=TA_CENTER,
        fontSize=12,
        textColor=colors.HexColor("#4b5563"),
        spaceAfter=18,
    )
    header_style = ParagraphStyle(
        name="Header",
        parent=styles["Heading2"],
        textColor=colors.HexColor("#1f4e79"),
        spaceAfter=10,
    )
    normal_style = ParagraphStyle(
        name="Normal",
        parent=styles["BodyText"],
        fontSize=11,
        leading=15,
        spaceAfter=8,
    )
    remark_style = ParagraphStyle(
        name="Remark",
        parent=styles["BodyText"],
        fontSize=10,
        leading=14,
        textColor=colors.HexColor("#1f2937"),
    )

    story = []

    logo_path = "download.jpeg"
    if os.path.exists(logo_path):
        logo_image = Image(logo_path, width=90, height=90)
    else:
        logo_drawing = Drawing(90, 90)
        logo_drawing.add(Rect(0, 0, 90, 90, fillColor=colors.HexColor("#0b3d91"), strokeColor=colors.HexColor("#0b3d91")))
        logo_drawing.add(String(45, 45, "BBDU", fontSize=18, fillColor=colors.white, textAnchor="middle", fontName="Helvetica-Bold"))
        logo_drawing.add(String(45, 20, "Babu Banarasi Das", fontSize=8, fillColor=colors.white, textAnchor="middle"))
        logo_drawing.add(String(45, 10, "University", fontSize=8, fillColor=colors.white, textAnchor="middle"))
        logo_image = logo_drawing

    title_text = Paragraph("<b>Student Performance Review</b>", title_style)
    subtitle_text = Paragraph(
        "Presented by Babu Banarasi Das University - Academic Monitoring Office",
        subtitle_style,
    )

    header_table = Table(
        [[logo_image, title_text], ["", subtitle_text]],
        colWidths=[110, 330],
        style=TableStyle(
            [
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("LEFTPADDING", (0, 0), (-1, -1), 0),
                ("RIGHTPADDING", (0, 0), (-1, -1), 0),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
            ]
        ),
    )
    story.append(header_table)
    story.append(Spacer(1, 8))

    profile_drawing = Drawing(90, 90)
    profile_drawing.add(Circle(45, 45, 42, fillColor=colors.HexColor("#f3f4f6"), strokeColor=colors.HexColor("#9ca3af")))
    profile_drawing.add(String(45, 50, student_info["Student Name"][0:1].upper(), fontSize=36, fillColor=colors.HexColor("#0b3d91"), textAnchor="middle", fontName="Helvetica-Bold"))
    profile_drawing.add(String(45, 15, "Student Photo", fontSize=8, fillColor=colors.HexColor("#6b7280"), textAnchor="middle"))

    risk_color = colors.HexColor("#16a34a") if student_info["Risk"] == "Low" else (
        colors.HexColor("#f59e0b") if student_info["Risk"] == "Medium" else colors.HexColor("#dc2626")
    )
    risk_text = Paragraph(
        f"<b>Risk Status:</b> <font color='{risk_color.hexval()}'>{student_info['Risk']}</font>",
        normal_style,
    )

    info_table = Table(
        [
            [profile_drawing, Paragraph(f"<b>Name:</b> {student_info['Student Name']}<br/>"
                                       f"<b>Student ID:</b> {student_info['Student ID']}<br/>"
                                       f"<b>Attendance:</b> {student_info['Attendance']}%<br/>"
                                       f"<b>Study Hours:</b> {student_info['Study Hours']}<br/>"
                                       f"<b>Previous Marks:</b> {student_info['Previous Marks']}<br/>"
                                       f"<b>Predicted Marks:</b> {student_info['Predicted Marks']:.2f}", normal_style), risk_text],
        ],
        colWidths=[110, 330],
        style=TableStyle([
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("LEFTPADDING", (0, 0), (-1, -1), 0),
            ("RIGHTPADDING", (0, 0), (-1, -1), 0),
        ]),
    )
    story.append(info_table)
    story.append(Spacer(1, 18))

    chart_title = Paragraph("Performance Insights", header_style)
    story.append(chart_title)

    pie = Pie()
    pie.x = 65
    pie.y = 0
    pie.width = 120
    pie.height = 120
    pie.data = [student_info["Attendance"], max(0, 100 - student_info["Attendance"])]
    pie.labels = ["Attendance", "Absent"]
    pie.slices.strokeWidth = 0.5
    pie.slices[0].fillColor = colors.HexColor("#0b8bff")
    pie.slices[1].fillColor = colors.HexColor("#c7d2fe")

    line_chart = LinePlot()
    line_chart.x = 50
    line_chart.y = 20
    line_chart.height = 130
    line_chart.width = 320
    line_chart.data = [[(0, student_info["Previous Marks"]), (1, student_info["Predicted Marks"])]]
    line_chart.strokeColor = colors.HexColor("#0b3d91")
    line_chart.lines[0].strokeColor = colors.HexColor("#0b3d91")
    line_chart.xValueAxis.valueMin = 0
    line_chart.xValueAxis.valueMax = 1
    line_chart.xValueAxis.valueStep = 1
    line_chart.xValueAxis.labelTextFormat = ["Previous", "Predicted"]
    line_chart.yValueAxis.valueMin = 0
    line_chart.yValueAxis.valueMax = 100
    line_chart.yValueAxis.valueStep = 25

    chart_drawing = Drawing(420, 160)
    chart_drawing.add(Rect(0, 0, 420, 160, fillColor=colors.HexColor("#f8fafc"), strokeColor=colors.HexColor("#e2e8f0")))
    chart_drawing.add(pie)
    chart_drawing.add(line_chart)
    chart_drawing.add(String(220, 145, "Attendance Distribution & Performance Trend", fontSize=11, fillColor=colors.HexColor("#0f172a"), textAnchor="middle"))

    story.append(chart_drawing)
    story.append(Spacer(1, 20))

    story.append(Paragraph("Performance Summary", header_style))
    story.append(Paragraph(student_info["Performance Summary"], normal_style))
    story.append(Paragraph("Recommendations", header_style))
    story.append(Paragraph(student_info["Recommendations"], remark_style))
    story.append(Spacer(1, 20))

    qr_value = f"{student_info['Student ID']}|{student_info['Student Name']}|{student_info['Risk']}|{datetime.now().strftime('%Y-%m-%d')}"
    qr_code = qr.QrCodeWidget(qr_value)
    bounds = qr_code.getBounds()
    qr_width = bounds[2] - bounds[0]
    qr_height = bounds[3] - bounds[1]
    qr_drawing = Drawing(80, 80)
    qr_drawing.add(qr_code)
    qr_code.x = 0
    qr_code.y = 0
    qr_code.barWidth = 1

    footer_table = Table(
        [
            [qr_drawing, Paragraph("<b>Teacher Remarks:</b><br/>"
                                   "Excellent work on attendance and consistent effort."
                                   " Continue to maintain this momentum.", remark_style)],
            ["", Paragraph("<br/><br/>__________________________<br/>Principal Signature", normal_style)],
        ],
        colWidths=[100, 340],
        style=TableStyle([
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("LEFTPADDING", (0, 0), (-1, -1), 0),
            ("RIGHTPADDING", (0, 0), (-1, -1), 0),
            ("TOPPADDING", (0, 1), (-1, 1), 20),
        ]),
    )
    story.append(footer_table)

    doc.build(story)
    buffer.seek(0)
    return buffer.read()


def render_predict(cursor, model):
    st.subheader("🔮 Predict Student Marks")
    student_name = st.text_input("Student Name", key="predict_student_name")
    student_id = st.text_input("Student ID", key="predict_student_id")
    attendance = st.number_input("Attendance (%)", 0, 100, 0, key="predict_attendance")
    study_hours = st.number_input("Study Hours", 0, 15, 0, key="predict_study_hours")
    previous_marks = st.number_input("Previous Marks", 0, 100, 0, key="predict_previous_marks")

    if st.button("Predict", key="predict_button"):
        input_df = pd.DataFrame(
            [
                {
                    "Attendance": attendance,
                    "StudyHours": study_hours,
                    "PreviousMarks": previous_marks,
                }
            ]
        )
        prediction = float(model.predict(input_df)[0])

        st.metric("Predicted Marks", f"{prediction:.2f}")
        st.write("Student Name:", student_name)
        st.write("Student ID:", student_id)
        st.success(f"Predicted Marks: {prediction:.2f}")

        if attendance >= 90:
            st.write("Attendance: Excellent")
        elif attendance >= 75:
            st.write("Attendance: Good")
        elif attendance >= 60:
            st.write("Attendance: Average")
        else:
            st.write("Attendance: Poor")

        st.subheader("Attendance Progress")
        st.progress(int(attendance))

        if prediction >= 70:
            risk = "Low"
            st.success("Low Risk")
        elif prediction >= 50:
            risk = "Medium"
            st.warning("Medium Risk")
        else:
            risk = "High"
            st.error("High Risk")

        st.subheader("🤖 AI Recommendation System")
        recommendations = []
        if attendance < 75:
            recommendations.append("Improve attendance to increase learning consistency.")
        if previous_marks < 60:
            recommendations.append("Strengthen foundational topics before the next exam.")
        if study_hours < 5:
            recommendations.append("Increase daily study hours with a structured study plan.")
        if risk == "High":
            recommendations.append("Schedule a review session with a tutor or teacher.")
        if risk == "Low":
            recommendations.append("Maintain current routines and challenge yourself with higher goals.")
        if not recommendations:
            recommendations.append("Keep up the strong habits and continue refining performance.")

        for item in recommendations:
            st.write(f"- {item}")

        cursor.execute(
            """
            INSERT INTO students
            (name, student_id, attendance, study_hours, previous_marks, predicted_marks, risk)
            VALUES(?,?,?,?,?,?,?)
            """,
            (
                student_name,
                student_id,
                attendance,
                study_hours,
                previous_marks,
                round(prediction, 2),
                risk,
            ),
        )
        cursor.connection.commit()

        result = pd.DataFrame(
            [
                {
                    "Student Name": student_name,
                    "Student ID": student_id,
                    "Attendance": attendance,
                    "Study Hours": study_hours,
                    "Previous Marks": previous_marks,
                    "Predicted Marks": round(prediction, 2),
                }
            ]
        )
        csv = result.to_csv(index=False).encode("utf-8")

        summary = "Based on the predicted marks, this student is in a "
        summary += "low-risk category." if risk == "Low" else (
            "medium-risk category." if risk == "Medium" else "high-risk category."
        )
        summary += " The student should continue focusing on consistent attendance and study routines."

        recommendations = []
        if attendance < 75:
            recommendations.append("Improve attendance to increase learning consistency.")
        if previous_marks < 60:
            recommendations.append("Strengthen foundational topics before the next exam.")
        if study_hours < 5:
            recommendations.append("Increase daily study hours with a structured plan.")
        if not recommendations:
            recommendations.append("Keep up the strong habits and continue refining performance.")

        pdf_info = {
            "Student Name": student_name,
            "Student ID": student_id,
            "Attendance": attendance,
            "Study Hours": study_hours,
            "Previous Marks": previous_marks,
            "Predicted Marks": round(prediction, 2),
            "Risk": risk,
            "Performance Summary": summary,
            "Recommendations": " ".join(recommendations),
        }
        pdf_data = generate_pdf_report(pdf_info)

        st.download_button(
            label="Download Report (CSV)",
            data=csv,
            file_name="student_report.csv",
            mime="text/csv",
        )
        st.download_button(
            label="Download Report (PDF)",
            data=pdf_data,
            file_name="student_report.pdf",
            mime="application/pdf",
        )

        history_entry = {
            "Name": student_name,
            "ID": student_id,
            "Attendance": attendance,
            "Study Hours": study_hours,
            "Previous Marks": previous_marks,
            "Predicted Marks": round(prediction, 2),
        }
        save_history_entry(history_entry)
        st.balloons()
    else:
        st.info("Enter student details and click Predict to see the result.")
