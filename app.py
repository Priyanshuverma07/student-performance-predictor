import os
import streamlit as st

from auth_view import render_login
from common import get_dashboard_dataframe, init_db, load_model
from dashboard_view import render_dashboard
from search_view import render_search
from update_view import render_update
from predict_view import render_predict
from bulk_view import render_bulk
from database_view import render_database
from delete_view import render_delete

st.set_page_config(
    page_title="Student Performance Predictor",
    page_icon="🎓",
    layout="centered",
)

st.markdown(
    """
    <style>
    .stApp {
        background: linear-gradient(135deg, #0f172a, #1e293b, #334155);
    }

    section[data-testid="stSidebar"] {
        background: rgba(17, 24, 39, 0.95);
        backdrop-filter: blur(14px);
        border-right: 1px solid rgba(56, 189, 248, 0.2);
    }

    h1 {
        color: white;
        text-align: center;
        font-weight: 700;
        background: linear-gradient(90deg, #38bdf8, #818cf8);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    h2, h3 {
        color: #38bdf8;
    }

    label, p, div, span {
        color: white !important;
    }

    .stButton > button {
        background: linear-gradient(90deg, #2563eb, #3b82f6);
        color: white;
        border-radius: 10px;
        height: 45px;
        width: 100%;
        font-weight: bold;
        border: none;
        transition: all 0.2s ease-in-out;
        box-shadow: 0 4px 12px rgba(37, 99, 235, 0.25);
    }

    .stButton > button:hover {
        background: linear-gradient(90deg, #1d4ed8, #2563eb);
        color: white;
        transform: translateY(-1px);
    }

    .stTextInput input, .stNumberInput input {
        background: rgba(30, 41, 59, 0.9);
        color: white;
        border-radius: 8px;
        border: 1px solid #475569;
    }

    div[data-testid="metric-container"] {
        background: rgba(30, 41, 59, 0.9);
        padding: 15px;
        border-radius: 12px;
        border: 1px solid rgba(56, 189, 248, 0.35);
        box-shadow: 0 6px 18px rgba(0, 0, 0, 0.2);
        transition: transform 0.2s ease-in-out;
    }

    div[data-testid="metric-container"]:hover {
        transform: translateY(-2px);
    }
    </style>
    """,
    unsafe_allow_html=True,
)

conn, cursor = init_db()

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "selected_section" not in st.session_state:
    st.session_state.selected_section = "Dashboard"
if "username" not in st.session_state:
    st.session_state.username = ""

if not render_login():
    st.stop()

model = load_model()

st.title("AI Student Performance Predictor")
st.markdown("---")

with st.sidebar:
    st.title("Navigation")
    st.info(f"👤 Logged in as: {st.session_state.username}")

    if st.button("📊 Dashboard", use_container_width=True, key="nav_dashboard"):
        st.session_state.selected_section = "Dashboard"
    if st.button("🔍 Search Student", use_container_width=True, key="nav_search"):
        st.session_state.selected_section = "Search"
    if st.button("✏️ Update Student", use_container_width=True, key="nav_update"):
        st.session_state.selected_section = "Update"
    if st.button("🔮 Predict", use_container_width=True, key="nav_predict"):
        st.session_state.selected_section = "Predict"
    if st.button("📦 Bulk Prediction", use_container_width=True, key="nav_bulk"):
        st.session_state.selected_section = "Bulk"
    if st.button("�️ Delete Student", use_container_width=True, key="nav_delete"):
        st.session_state.selected_section = "Delete"
    if st.button("�🗂️ Database", use_container_width=True, key="nav_database"):
        st.session_state.selected_section = "Database"

    st.markdown("---")
    st.title("About")
    st.write("This AI model predicts student performance using Machine Learning.")
    if st.button("Logout", use_container_width=True, key="logout_button"):
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.session_state.selected_section = "Dashboard"
        st.rerun()

dashboard = get_dashboard_dataframe(cursor)

if st.session_state.selected_section == "Dashboard":
    render_dashboard(dashboard)
elif st.session_state.selected_section == "Search":
    render_search(cursor)
elif st.session_state.selected_section == "Update":
    render_update(cursor, model)
elif st.session_state.selected_section == "Predict":
    render_predict(cursor, model)
elif st.session_state.selected_section == "Bulk":
    render_bulk(model)
elif st.session_state.selected_section == "Delete":
    render_delete(cursor)
elif st.session_state.selected_section == "Database":
    render_database(dashboard)
