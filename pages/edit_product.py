import streamlit as st
from components.vendor_sidebar import show_vendor_sidebar
from services.product_service import update_product

st.set_page_config(
    page_title="Edit Product",
    page_icon="✏️",
    layout="wide"
)

# Protect page
if "logged_in" not in st.session_state or not st.session_state["logged_in"]:
    st.warning("Please log in first.")
    st.switch_page("pages/login.py")

vendor = st.session_state["vendor"]

show_vendor_sidebar()

st.title("✏️ Edit Product")

if "editing_product" not in st.session_state:
    st.warning("No product selected.")
    st.switch_page("pages/my_products.py")


product = st.session_state["editing_product"]

product_id = product[0]

new_name = st.text_input(
    "Product Name",
    value=product[1]
)

new_description = st.text_area(
    "Description",
    value=product[2] or ""
)

new_price = st.number_input(
    "Price (₦)",
    min_value=0.0,
    value=float(product[3]),
    step=100.0
)

new_stock = st.number_input(
    "Stock Quantity",
    min_value=0,
    value=int(product[4]),
    step=1
)


if st.button(
    "💾 Save Changes",
    use_container_width=True
):

    if not new_name.strip():
        st.error("Product name cannot be empty.")

    elif new_price <= 0:
        st.error("Price must be greater than ₦0.")

    else:

        update_product(
            product_id,
            vendor["id"],
            new_name,
            new_description,
            new_price,
            new_stock
        )

        st.success(
            "Product updated successfully!"
        )

        del st.session_state["editing_product"]

        st.switch_page(
            "pages/my_products.py"
        )