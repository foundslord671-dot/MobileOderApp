import streamlit as st


def show_vendor_sidebar():
    st.sidebar.title("🏪 Vendor Panel")

    if st.sidebar.button("📊 Dashboard", use_container_width=True):
        st.switch_page("pages/vendor_dashboard.py")

    if st.sidebar.button("📦 Add Product", use_container_width=True):
        st.switch_page("pages/add_product.py")

    if st.sidebar.button("📋 My Products", use_container_width=True):
        st.switch_page("pages/my_products.py")

    if st.sidebar.button("🛒 Orders", use_container_width=True):
        st.info("Orders will be added in Version 0.5")

    if st.sidebar.button("📈 Analytics", use_container_width=True):
        st.info("Analytics will be added in a future version")

    if st.sidebar.button("⚙️ Settings", use_container_width=True):
        st.info("Settings will be added in a future version")

    st.sidebar.divider()

    if st.sidebar.button("🚪 Logout", use_container_width=True):
        st.session_state.clear()
        st.switch_page("pages/login.py")