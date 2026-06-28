import streamlit as st

from components.admin_sidebar import show_admin_sidebar

from services.admin_service import (
    get_all_products,
    delete_product
)


st.set_page_config(
    page_title="Manage Products",
    page_icon="📦",
    layout="wide"
)


# Protect page
if "logged_in" not in st.session_state or not st.session_state["logged_in"]:
    st.warning("Please log in first.")
    st.switch_page("pages/login.py")


user = st.session_state["vendor"]


if not user["is_admin"]:
    st.error("Access denied. Admins only.")
    st.stop()


show_admin_sidebar()


st.title("📦 Manage Products")


products = get_all_products()


if not products:

    st.info("No products found.")


else:

    st.success(
        f"{len(products)} product(s) found."
    )

    st.divider()


    for product in products:

        product_id = product[0]
        product_name = product[1]
        description = product[2]
        price = product[3]
        stock = product[4]
        vendor_name = product[5]
        created_at = product[6]


        with st.container(border=True):

            st.subheader(product_name)

            st.write(
                f"🏪 Vendor: {vendor_name}"
            )

            st.write(
                f"💰 Price: ₦{price:,.2f}"
            )

            st.write(
                f"📦 Stock: {stock}"
            )

            if description:

                st.write(
                    f"📝 {description}"
                )


            st.write(
                f"🕒 Added: {created_at}"
            )


            if st.button(
                "🗑 Delete Product",
                key=f"delete_{product_id}"
            ):

                deleted = delete_product(product_id)

                if deleted:

                    st.success(
                        "Product deleted."
                    )

                    st.rerun()

                else:

                    st.error(
                        "Failed to delete product."
                    )