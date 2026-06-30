import streamlit as st


def render_search(cursor):
    st.subheader("🔍 Search Student")
    search_id = st.text_input("Enter Student ID", key="search_student_id")
    if st.button("Search", key="search_student_button"):
        cursor.execute("SELECT * FROM students WHERE student_id=?", (search_id,))
        result = cursor.fetchone()
        if result:
            st.success("Student Found")
            st.write("Name :", result[1])
            st.write("Student ID :", result[2])
            st.write("Attendance :", result[3])
            st.write("Study Hours :", result[4])
            st.write("Previous Marks :", result[5])
            st.write("Predicted Marks :", result[6])
            st.write("Risk :", result[7])
        else:
            st.error("Student Not Found")
