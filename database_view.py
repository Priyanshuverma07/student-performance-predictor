import io
import pandas as pd
import streamlit as st


def render_database(dashboard):
    st.subheader("Student Database")
    st.dataframe(dashboard)

    if not dashboard.empty:
        buffer = io.BytesIO()
        try:
            with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
                dashboard.to_excel(writer, index=False, sheet_name="Students")
            buffer.seek(0)
            st.download_button(
                label="📥 Export Database to Excel",
                data=buffer,
                file_name="student_database.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True,
            )
        except Exception:
            csv_data = dashboard.to_csv(index=False).encode("utf-8")
            st.warning("Excel export is unavailable in this environment, downloading CSV instead.")
            st.download_button(
                label="📥 Download Database as CSV",
                data=csv_data,
                file_name="student_database.csv",
                mime="text/csv",
                use_container_width=True,
            )
    else:
        st.info("No student records available to export.")
