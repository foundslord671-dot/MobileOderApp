import streamlit as st

from database.models import create_tables
from components.customer_store import show_customer_store


# Create database tables
create_tables()


st.set_page_config(
    page_title="Mobile Order App",
    page_icon="🛒",
    layout="wide"
)


# -----------------------------
# Check if a store link was used
# -----------------------------

store = st.query_params.get("store")

if isinstance(store, list):
    store = store[0]


if store:

    show_customer_store()

else:

    st.title("🛒 Mobile Order App")

    st.write("""
Welcome to the Mobile Order App.

Choose a page from the sidebar to continue.
""")

    st.sidebar.title("Navigation")

    st.sidebar.success(
        "Select a page from the sidebar."
    )