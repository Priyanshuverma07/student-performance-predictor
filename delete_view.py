import streamlit as st


def render_delete(cursor):
    st.subheader("🗑️ Delete Student")
    delete_id = st.text_input("Enter Student ID to delete", key="delete_student_id")

    if st.button("Delete Student", key="delete_student_button"):
        if not delete_id.strip():
            st.error("Please enter a student ID to delete.")
            return

        cursor.execute("DELETE FROM students WHERE student_id=?", (delete_id.strip(),))
        cursor.connection.commit()

        if cursor.rowcount > 0:
            st.success(f"Student with ID {delete_id} has been deleted.")
        else:
            st.warning("No student found with that ID.")

    st.info("Use this tool to remove a student record permanently from the database.")
