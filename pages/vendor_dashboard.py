import streamlit as st

from components.vendor_sidebar import show_vendor_sidebar

from services.product_service import get_product_statistics

from services.order_service import (
    get_vendor_statistics,
    get_recent_vendor_orders
)


st.set_page_config(
    page_title="Vendor Dashboard",
    page_icon="🏪",
    layout="wide"
)


# Protect page
if "logged_in" not in st.session_state or not st.session_state["logged_in"]:
    st.warning("Please log in first.")
    st.switch_page("pages/login.py")


vendor = st.session_state["vendor"]


show_vendor_sidebar()


st.title(
    f"🏪 Welcome, {vendor['business_name']}"
)

st.write(
    f"👤 Owner: **{vendor['owner_name']}**"
)

st.write(
    f"📧 Email: **{vendor['email']}**"
)

st.write(
    f"🏷 Store Username: **{vendor['store_username']}**"
)


st.divider()


# Product statistics
product_stats = get_product_statistics(
    vendor["id"]
)

total_products = product_stats[0]
total_stock = product_stats[1]
inventory_value = product_stats[2]


# Order statistics
order_stats = get_vendor_statistics(
    vendor["id"]
)

total_orders = order_stats[0]
total_revenue = order_stats[1]


col1, col2, col3, col4, col5 = st.columns(5)


with col1:

    st.metric(
        "📦 Products",
        total_products
    )


with col2:

    st.metric(
        "📊 Stock",
        total_stock
    )


with col3:

    st.metric(
        "💰 Inventory",
        f"₦{inventory_value:,.2f}"
    )


with col4:

    st.metric(
        "🛒 Orders",
        total_orders
    )


with col5:

    st.metric(
        "💵 Revenue",
        f"₦{total_revenue:,.2f}"
    )


st.divider()


st.subheader("🕒 Recent Orders")


recent_orders = get_recent_vendor_orders(
    vendor["id"]
)


if recent_orders:

    for order in recent_orders:

        customer = order[0]
        amount = order[1]
        status = order[2]
        date = order[3]

        with st.container(border=True):

            st.write(
                f"👤 Customer: **{customer}**"
            )

            st.write(
                f"💰 Amount: ₦{amount:,.2f}"
            )

            st.write(
                f"📦 Status: {status}"
            )

            st.write(
                f"🕒 {date}"
            )

else:

    st.info(
        "No recent orders."
    )


st.divider()


st.subheader("🔗 My Store Link")


store_link = (
    f"http://localhost:8501/store?store={vendor['store_username']}"
)


st.code(store_link)


st.info(
    "Share this link with your customers so they can shop directly from your store."
)


st.divider()


st.subheader("Welcome!")


st.write(
    """
Welcome to your vendor dashboard.

Use the navigation menu to:

- 📦 Add Products
- 📋 Manage Products
- 🛒 View Orders
- 📊 Monitor Sales
- ⚙️ Manage Your Store
"""
)