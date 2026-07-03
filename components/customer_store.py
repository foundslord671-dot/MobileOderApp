import streamlit as st
import urllib.parse

from services.auth_service import get_vendor_by_username
from services.product_service import (
    get_all_products,
    add_review,
    get_product_reviews,
    get_product_rating,
)
from services.cart_service import add_to_cart


def show_customer_store():
    """
    Public customer storefront.

    Opens a vendor's store from:
        ?store=vendor_username
    """

    # -----------------------------
    # Get vendor username
    # -----------------------------
    store_username = st.query_params.get("store")

    if not store_username:

        st.title("🛒 Mobile Order App")

        st.write(
            """
            Welcome!

            This is the Mobile Order App marketplace.

            To visit a vendor's store,
            use the store link shared by the vendor.
            """
        )

        st.info("No store selected.")

        return

    # -----------------------------
    # Find vendor
    # -----------------------------
    vendor = get_vendor_by_username(store_username)

    if vendor is None:

        st.error("Store not found.")

        return

    vendor_id = vendor[0]
    business_name = vendor[1]
    phone = vendor[4]

    # -----------------------------
    # Store Header
    # -----------------------------
    st.title(f"🏪 {business_name}")

    st.write(
        "Browse our products below."
    )

    st.divider()

    # -----------------------------
    # WhatsApp helper
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
    # Load products
    # -----------------------------
    products = get_all_products()

    vendor_products = []

    for product in products:

        if product[7] == store_username:

            vendor_products.append(product)

    if not vendor_products:

        st.info(
            "This store has no products yet."
        )

        return# -----------------------------
    # Display Products
    # -----------------------------

    for product in vendor_products:

        product_id = product[0]
        name = product[1]
        description = product[2]
        price = product[3]
        stock = product[4]
        image = product[5]

        with st.container(border=True):

            col1, col2 = st.columns([1, 2])

            with col1:

                if image:
                    st.image(
                        image,
                        use_container_width=True
                    )
                else:
                    st.caption("No image available")

            with col2:

                st.subheader(name)

                st.write(description)

                st.write(
                    f"💰 **₦{price:,.2f}**"
                )

                st.write(
                    f"📦 Stock: {stock}"
                )

                rating, count = get_product_rating(
                    product_id
                )

                st.write(
                    f"⭐ {round(rating,1)} ({count} reviews)"
                )

                cart_product = {
                    "id": product_id,
                    "name": name,
                    "price": price,
                    "image": image
                }

                if st.button(
                    "🛒 Add to Cart",
                    key=f"cart_{product_id}",
                    use_container_width=True
                ):

                    add_to_cart(cart_product)

                    st.success(
                        "Added to cart."
                    )

                whatsapp_link = whatsapp_order(
                    {
                        "name": name,
                        "price": price
                    }
                )

                st.link_button(
                    "📱 Order on WhatsApp",
                    whatsapp_link,
                    use_container_width=True
                )

        st.subheader("⭐ Customer Reviews")

        reviews = get_product_reviews(
            product_id
        )

        if reviews:

            for review in reviews:

                customer = review[0]
                stars = review[1]
                text = review[2]
                date = review[3]

                with st.container(border=True):

                    st.write(
                        f"**{customer}** • ⭐ {stars}/5"
                    )

                    st.write(text)

                    st.caption(str(date))

        else:

            st.info(
                "No reviews yet."
            )
            # -----------------------------
        # Leave a Review
        # -----------------------------

        with st.expander("✍ Leave a Review"):

            customer_name = st.text_input(
                "Your Name",
                key=f"name_{product_id}"
            )

            rating = st.slider(
                "Rating",
                min_value=1,
                max_value=5,
                value=5,
                key=f"rating_{product_id}"
            )

            review_text = st.text_area(
                "Your Review",
                key=f"review_{product_id}"
            )

            if st.button(
                "Submit Review",
                key=f"submit_{product_id}",
                use_container_width=True
            ):

                if customer_name.strip() and review_text.strip():

                    success = add_review(
                        product_id,
                        vendor_id,
                        customer_name.strip(),
                        rating,
                        review_text.strip()
                    )

                    if success:

                        st.success(
                            "✅ Thank you! Your review has been submitted."
                        )

                        st.rerun()

                    else:

                        st.error(
                            "Could not submit your review."
                        )

                else:

                    st.warning(
                        "Please enter your name and review."
                    )

        st.divider()

    # -----------------------------
    # Footer
    # -----------------------------

    st.caption(
        f"Shopping at {business_name}"
    )