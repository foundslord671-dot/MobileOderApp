import streamlit as st

from components.vendor_sidebar import show_vendor_sidebar
from services.order_service import (
    get_vendor_orders,
    update_order_status,
    get_order_items
)


st.set_page_config(
    page_title="Vendor Orders",
    page_icon="🛒",
    layout="wide"
)


# Protect page
if "logged_in" not in st.session_state or not st.session_state["logged_in"]:
    st.warning("Please log in first.")
    st.switch_page("pages/login.py")


vendor = st.session_state["vendor"]


show_vendor_sidebar()


st.title("🛒 Customer Orders")


orders = get_vendor_orders(vendor["id"])


if not orders:

    st.info("You have no orders yet.")

else:

    st.success(f"You have {len(orders)} order(s).")

    st.divider()


    for order in orders:

        order_id = order[0]
        customer_name = order[1]
        customer_phone = order[2]
        customer_address = order[3]
        total_amount = order[4]
        status = order[5]
        created_at = order[6]


        with st.container(border=True):

            st.subheader(f"Order #{order_id}")

            st.write(f"👤 Customer: {customer_name}")
            st.write(f"📞 Phone: {customer_phone}")
            st.write(f"📍 Address: {customer_address}")

            st.divider()

            st.write("📦 Products:")

            items = get_order_items(order_id)

            if items:

                for item in items:

                    product_name = item[0]
                    quantity = item[1]
                    price = item[2]

                    st.write(
                        f"- {product_name} × {quantity} "
                        f"(₦{price:,.2f} each)"
                    )

            else:

                st.write("No product details found.")


            st.divider()


            st.write(
                f"💰 Total: ₦{total_amount:,.2f}"
            )


            new_status = st.selectbox(
                "Update Status",
                [
                    "Pending",
                    "Confirmed",
                    "Delivered",
                    "Cancelled"
                ],
                index=[
                    "Pending",
                    "Confirmed",
                    "Delivered",
                    "Cancelled"
                ].index(status)
                if status in [
                    "Pending",
                    "Confirmed",
                    "Delivered",
                    "Cancelled"
                ]
                else 0,
                key=f"status_{order_id}"
            )


            if st.button(
                "💾 Save Status",
                key=f"save_{order_id}"
            ):

                updated = update_order_status(
                    order_id,
                    vendor["id"],
                    new_status
                )

                if updated:
                    st.success("Order status updated!")
                    st.rerun()

                else:
                    st.error("Failed to update status.")


            st.write(f"🕒 Date: {created_at}")