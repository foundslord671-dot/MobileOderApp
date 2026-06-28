import streamlit as st
from database.models import create_tables

# Create database tables automatically
create_tables()

st.set_page_config(
    page_title="Mobile Order App",
    page_icon="🛒",
    layout="wide"
)

st.title("🛒 Mobile Order App")

st.write("""
Welcome to the Mobile Order App.

Choose a page from the sidebar to continue.
""")

st.sidebar.title("Navigation")
st.sidebar.success("Select a page from the sidebar.")