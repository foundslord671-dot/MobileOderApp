import streamlit as st
from components.vendor_sidebar import show_vendor_sidebar
from services.product_service import (
    get_vendor_products,
    delete_product
)

st.set_page_config(
    page_title="My Products",
    page_icon="📋",
    layout="wide"
)

# Protect page
if "logged_in" not in st.session_state or not st.session_state["logged_in"]:
    st.warning("Please log in first.")
    st.switch_page("pages/login.py")


vendor = st.session_state["vendor"]

show_vendor_sidebar()

st.title("📋 My Products")


# Search box
search = st.text_input(
    "🔍 Search products",
    placeholder="Enter product name..."
)


products = get_vendor_products(vendor["id"])


# Filter products
if search:

    products = [
        product for product in products
        if search.lower() in product[1].lower()
    ]


if not products:

    st.info("No products found.")

else:

    cols = st.columns(3)

    for index, product in enumerate(products):

        product_id = product[0]
        product_name = product[1]
        description = product[2]
        price = product[3]
        stock = product[4]
        image_url = product[5]


        with cols[index % 3]:

            with st.container(border=True):

                if image_url:

                    st.image(
                        image_url,
                        use_container_width=True
                    )


                st.subheader(product_name)


                if description:
                    st.write(description)


                st.write(f"💰 ₦{price}")
                st.write(f"📦 Stock: {stock}")


                col1, col2 = st.columns(2)


                with col1:

                    if st.button(
                        "✏️ Edit",
                        key=f"edit_{product_id}",
                        use_container_width=True
                    ):

                        st.session_state["editing_product"] = product

                        st.switch_page(
                            "pages/edit_product.py"
                        )


                with col2:

                    if st.button(
                        "🗑 Delete",
                        key=f"delete_{product_id}",
                        use_container_width=True
                    ):

                        delete_product(
                            product_id,
                            vendor["id"]
                        )

                        st.success(
                            "Product deleted successfully!"
                        )

                        st.rerun()