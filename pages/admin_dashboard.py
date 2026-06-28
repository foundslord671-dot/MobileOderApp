import streamlit as st

from components.admin_sidebar import show_admin_sidebar
from services.admin_service import get_admin_statistics


st.set_page_config(
    page_title="Admin Dashboard",
    page_icon="👑",
    layout="wide"
)


# Protect page
if "logged_in" not in st.session_state or not st.session_state["logged_in"]:
    st.warning("Please log in first.")
    st.switch_page("pages/login.py")


user = st.session_state["vendor"]


# Check admin access
if not user["is_admin"]:
    st.error("Access denied. Admins only.")
    st.stop()


# Show admin sidebar
show_admin_sidebar()



st.title("👑 Admin Dashboard")


st.success(
    f"Welcome Admin, {user['owner_name']}"
)


st.divider()



# Get real statistics
stats = get_admin_statistics()

total_vendors = stats[0]
total_products = stats[1]
total_orders = stats[2]



st.subheader("📊 Platform Overview")


col1, col2, col3 = st.columns(3)


with col1:

    st.metric(
        "👥 Vendors",
        total_vendors
    )


with col2:

    st.metric(
        "📦 Products",
        total_products
    )


with col3:

    st.metric(
        "🛒 Orders",
        total_orders
    )



st.divider()


st.info(
    """
Admin dashboard connected successfully.

Use the sidebar to manage:

- 👥 Vendors
- 🛒 Orders
- 📦 Products
"""
)