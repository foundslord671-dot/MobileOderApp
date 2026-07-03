import streamlit as st

from database.models import create_tables
from components.customer_store import show_customer_store


# Create database tables (safe because your SQL uses IF NOT EXISTS)
create_tables()


st.set_page_config(
    page_title="Mobile Order App",
    page_icon="🛒",
    layout="wide"
)


show_customer_store()