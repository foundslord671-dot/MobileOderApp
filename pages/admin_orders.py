import streamlit as st

from components.admin_sidebar import show_admin_sidebar

from services.admin_service import (
    get_all_orders,
    get_order_items,
    update_order_status
)


st.set_page_config(
    page_title="All Orders",
    page_icon="🛒",
    layout="wide"
)


if "logged_in" not in st.session_state or not st.session_state["logged_in"]:
    st.warning("Please log in first.")
    st.switch_page("pages/login.py")


user = st.session_state["vendor"]


if not user["is_admin"]:
    st.error("Access denied. Admins only.")
    st.stop()


show_admin_sidebar()


st.title("🛒 All Orders")


orders = get_all_orders()


status_options = [
    "Pending",
    "Confirmed",
    "Delivered",
    "Cancelled"
]


if not orders:

    st.info("No orders found.")


else:

    st.success(
        f"{len(orders)} order(s) found."
    )

    st.divider()


    for order in orders:

        order_id = order[0]
        vendor_name = order[1]
        customer_name = order[2]
        customer_phone = order[3]
        customer_address = order[4]
        total_amount = order[5]
        status = order[6]
        created_at = order[7]


        with st.container(border=True):

            st.subheader(
                f"Order #{order_id}"
            )


            st.write(
                f"🏪 Vendor: {vendor_name}"
            )

            st.write(
                f"👤 Customer: {customer_name}"
            )

            st.write(
                f"📞 Phone: {customer_phone}"
            )

            st.write(
                f"📍 Address: {customer_address}"
            )

            st.write(
                f"💰 Total: ₦{total_amount:,.2f}"
            )

            st.write(
                f"📦 Current Status: {status}"
            )

            st.write(
                f"🕒 Date: {created_at}"
            )


            st.divider()


            st.subheader("📦 Products")


            items = get_order_items(order_id)


            if items:

                for item in items:

                    product_name = item[0]
                    quantity = item[1]
                    price = item[2]

                    st.write(
                        f"• {product_name} "
                        f"x{quantity} - ₦{price:,.2f}"
                    )

            else:

                st.info(
                    "No products found for this order."
                )


            st.divider()


            new_status = st.selectbox(
                "Update Status",
                status_options,

                index=status_options.index(status)
                if status in status_options
                else 0,

                key=f"status_{order_id}"
            )


            if st.button(
                "💾 Save Status",
                key=f"save_{order_id}"
            ):

                updated = update_order_status(
                    order_id,
                    new_status
                )

                if updated:

                    st.success(
                        "Order status updated."
                    )

                    st.rerun()

                else:

                    st.error(
                        "Failed to update status."
                    )