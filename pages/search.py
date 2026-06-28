import streamlit as st

from services.product_service import search_products
from services.cart_service import add_to_cart


st.set_page_config(
    page_title="Search Products",
    page_icon="🔍"
)


st.title("🔍 Search Products")


keyword = st.text_input(
    "Search for products or stores"
)



if keyword:


    products = search_products(keyword)


    if not products:

        st.info(
            "No products found."
        )


    else:


        st.success(
            f"{len(products)} product(s) found"
        )


        for product in products:


            product_id = product[0]
            name = product[1]
            description = product[2]
            price = product[3]
            stock = product[4]
            image = product[5]
            business_name = product[6]
            store_username = product[7]


            st.divider()


            col1, col2 = st.columns([1,2])


            with col1:

                if image:

                    st.image(
                        image,
                        use_container_width=True
                    )


            with col2:


                st.subheader(name)


                st.write(description)


                st.write(
                    f"💰 Price: ₦{price}"
                )


                st.write(
                    f"🏪 Seller: {business_name}"
                )


                cart_product = {

                    "id": product_id,

                    "name": name,

                    "price": price,

                    "image": image

                }


                if st.button(
                    "🛒 Add to Cart",
                    key=f"cart_{product_id}"
                ):

                    add_to_cart(cart_product)

                    st.success(
                        "Added to cart"
                    )


                st.page_link(
                    "pages/store.py",
                    label="🏪 Visit Store",
                    query_params={
                        "store": store_username
                    }
                )