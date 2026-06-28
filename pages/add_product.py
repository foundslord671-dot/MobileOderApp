import streamlit as st

from database.connection import get_connection


st.set_page_config(
    page_title="Add Product",
    page_icon="📦",
    layout="wide"
)


# Protect page
if "logged_in" not in st.session_state or not st.session_state["logged_in"]:
    st.warning("Please log in first.")
    st.switch_page("pages/login.py")


vendor = st.session_state["vendor"]


st.title("📦 Add Product")

st.write(
    f"Adding product for: {vendor['business_name']}"
)


st.divider()


product_name = st.text_input(
    "Product Name"
)


description = st.text_area(
    "Description"
)


price = st.number_input(
    "Price (₦)",
    min_value=0.0,
    step=100.0
)


stock = st.number_input(
    "Stock Quantity",
    min_value=0,
    step=1
)


image_url = st.text_input(
    "Image URL (optional)"
)



if st.button(
    "✅ Add Product",
    use_container_width=True
):

    if not product_name:

        st.error(
            "Please enter product name."
        )

    elif price <= 0:

        st.error(
            "Price must be greater than zero."
        )

    else:

        try:

            conn = get_connection()
            cur = conn.cursor()


            cur.execute(
                """
                INSERT INTO products
                (
                    vendor_id,
                    product_name,
                    description,
                    price,
                    stock,
                    image_url
                )

                VALUES
                (%s,%s,%s,%s,%s,%s)
                """,

                (
                    vendor["id"],
                    product_name,
                    description,
                    price,
                    stock,
                    image_url
                )
            )


            conn.commit()

            cur.close()
            conn.close()


            st.success(
                "✅ Product added successfully!"
            )


        except Exception as e:

            st.error(
                "Failed to add product."
            )

            st.write(e)