import streamlit as st


def show_admin_sidebar():

    st.sidebar.title("👑 Admin Panel")


    if st.sidebar.button(
        "📊 Dashboard",
        use_container_width=True
    ):
        st.switch_page(
            "pages/admin_dashboard.py"
        )


    if st.sidebar.button(
        "👥 Manage Vendors",
        use_container_width=True
    ):
        st.switch_page(
            "pages/admin_vendors.py"
        )


    if st.sidebar.button(
        "📦 Manage Products",
        use_container_width=True
    ):
        st.switch_page(
            "pages/admin_products.py"
        )


    if st.sidebar.button(
        "🛒 All Orders",
        use_container_width=True
    ):
        st.switch_page(
            "pages/admin_orders.py"
        )


    st.sidebar.divider()


    if st.sidebar.button(
        "🚪 Logout",
        use_container_width=True
    ):

        st.session_state.clear()

        st.switch_page(
            "pages/login.py"
        )