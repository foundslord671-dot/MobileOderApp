import streamlit as st

from services.cart_service import (
    get_cart,
    get_cart_total,
    remove_from_cart,
    clear_cart
)

from services.order_service import create_order


st.set_page_config(
    page_title="Shopping Cart",
    page_icon="🛒",
    layout="wide"
)


st.title("🛒 Shopping Cart")


cart = get_cart()


if not cart:
    st.info("Your cart is empty.")
    st.stop()


# -----------------------------
# Cart Items
# -----------------------------

for item in cart:

    with st.container(border=True):

        st.subheader(item["name"])

        st.write(
            f"Price: ₦{item['price']:,.2f}"
        )

        st.write(
            f"Quantity: {item['quantity']}"
        )

        st.write(
            f"Subtotal: ₦{item['price'] * item['quantity']:,.2f}"
        )

        if st.button(
            "🗑 Remove",
            key=f"remove_{item['id']}"
        ):

            remove_from_cart(item["id"])

            st.rerun()


st.divider()


# -----------------------------
# Total + Clear Cart
# -----------------------------

total = get_cart_total()

col1, col2 = st.columns([3,1])

with col1:

    st.subheader(
        f"Total: ₦{total:,.2f}"
    )

with col2:

    if st.button(
        "🗑 Clear Cart",
        use_container_width=True
    ):

        clear_cart()

        st.success(
            "Cart cleared."
        )

        st.rerun()


st.divider()


# -----------------------------
# Customer Information
# -----------------------------

st.subheader(
    "Customer Information"
)


customer_name = st.text_input(
    "Full Name"
)

customer_phone = st.text_input(
    "Phone Number"
)

customer_address = st.text_area(
    "Delivery Address"
)


# -----------------------------
# Place Order
# -----------------------------

if st.button(
    "✅ Place Order",
    use_container_width=True
):

    if (
        not customer_name.strip()
        or not customer_phone.strip()
        or not customer_address.strip()
    ):

        st.error(
            "Please fill in all customer information."
        )

    else:

        if "vendor_id" not in cart[0]:

            st.error(
                """
This cart contains old products.

Please click **Clear Cart**, go back to the store,
add the products again, then place your order.
"""
            )

            st.stop()

        vendor_id = cart[0]["vendor_id"]

        success, result = create_order(

            vendor_id,

            customer_name.strip(),

            customer_phone.strip(),

            customer_address.strip(),

            cart

        )

        if success:

            order_number = result

            clear_cart()

            st.success(
                "🎉 Order placed successfully!"
            )

            st.balloons()

            st.divider()

            st.subheader(
                "🧾 Order Summary"
            )

            st.write(
                f"Order Number: **#{order_number}**"
            )

            st.write(
                f"Customer: **{customer_name}**"
            )

            st.write(
                f"Total: **₦{total:,.2f}**"
            )

            st.write(
                "Items Ordered:"
            )

            for item in cart:

                st.write(
                    f"• {item['name']} × {item['quantity']}"
                )

        else:

            st.error(result)