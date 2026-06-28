import streamlit as st
import urllib.parse

from services.auth_service import get_vendor_by_username

from services.product_service import (
    get_all_products,
    add_review,
    get_product_reviews,
    get_product_rating
)

from services.cart_service import add_to_cart


st.set_page_config(
    page_title="Store",
    page_icon="🛒"
)


# -----------------------------
# Get store username
# -----------------------------

query_params = st.query_params

store_username = query_params.get("store")


if not store_username:

    st.error("No store selected.")
    st.stop()



# -----------------------------
# Get vendor information
# -----------------------------

vendor = get_vendor_by_username(store_username)


if vendor is None:

    st.error("Store not found.")
    st.stop()



vendor_id = vendor[0]
business_name = vendor[1]
phone = vendor[4]



# -----------------------------
# Store Header
# -----------------------------

st.title(f"🏪 {business_name}")

st.write(
    "Welcome to our store. Browse products and order directly."
)



# -----------------------------
# WhatsApp link
# -----------------------------

def whatsapp_order(product):

    message = f"""
Hello {business_name},

I want to order:

Product: {product['name']}
Price: ₦{product['price']}

Please confirm availability.
"""

    encoded = urllib.parse.quote(message)

    return (
        f"https://wa.me/{phone}"
        f"?text={encoded}"
    )



# -----------------------------
# Get products
# -----------------------------

products = get_all_products()


vendor_products = []


for product in products:

    if product[7] == store_username:

        vendor_products.append(product)



if not vendor_products:

    st.info("This store has no products yet.")
    st.stop()



# -----------------------------
# Display products
# -----------------------------

for product in vendor_products:


    product_id = product[0]
    name = product[1]
    description = product[2]
    price = product[3]
    stock = product[4]
    image = product[5]



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
            f"📦 Stock: {stock}"
        )



        # Rating

        rating, count = get_product_rating(product_id)


        st.write(
            f"⭐ {round(rating,1)} "
            f"({count} reviews)"
        )



        # Add cart

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



        # WhatsApp

        link = whatsapp_order(
            {
                "name":name,
                "price":price
            }
        )


        st.markdown(
            f"""
            <a href="{link}" target="_blank">
            📱 Order on WhatsApp
            </a>
            """,
            unsafe_allow_html=True
        )



    # -----------------------------
    # Reviews section
    # -----------------------------


    st.subheader("💬 Reviews")


    reviews = get_product_reviews(product_id)



    if reviews:


        for review in reviews:


            customer = review[0]

            stars = review[1]

            text = review[2]

            date = review[3]


            st.write(
                f"⭐ {stars}/5 - {customer}"
            )

            st.write(text)

            st.caption(str(date))


    else:

        st.write(
            "No reviews yet."
        )



    # -----------------------------
    # Add review
    # -----------------------------


    with st.expander(
        "✍ Leave a review"
    ):


        customer_name = st.text_input(
            "Your name",
            key=f"name_{product_id}"
        )


        rating = st.slider(
            "Rating",
            1,
            5,
            5,
            key=f"rating_{product_id}"
        )


        review_text = st.text_area(
            "Your review",
            key=f"review_{product_id}"
        )



        if st.button(
            "Submit Review",
            key=f"submit_{product_id}"
        ):


            if customer_name and review_text:


                success = add_review(

                    product_id,

                    vendor_id,

                    customer_name,

                    rating,

                    review_text

                )


                if success:

                    st.success(
                        "Review submitted!"
                    )

                    st.rerun()


                else:

                    st.error(
                        "Could not submit review."
                    )


            else:

                st.warning(
                    "Please fill all fields."
                )