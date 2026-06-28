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


for item in cart:

    with st.container(border=True):

        st.subheader(item["name"])

        st.write(f"Price: ₦{item['price']:,.2f}")
        st.write(f"Quantity: {item['quantity']}")

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


total = get_cart_total()

st.subheader(f"Total: ₦{total:,.2f}")


st.divider()


st.subheader("Customer Information")


customer_name = st.text_input("Full Name")
customer_phone = st.text_input("Phone Number")
customer_address = st.text_area("Delivery Address")


if st.button(
    "✅ Place Order",
    use_container_width=True
):

    if (
        not customer_name
        or not customer_phone
        or not customer_address
    ):

        st.error("Please fill in all customer information.")


    else:

        vendor_id = cart[0]["vendor_id"]


        success, result = create_order(
            vendor_id,
            customer_name,
            customer_phone,
            customer_address,
            cart
        )


        if success:

            order_number = result

            st.success("🎉 Order placed successfully!")


            st.divider()


            st.subheader("🧾 Order Summary")

            st.write(
                f"Order Number: **#{order_number}**"
            )

            st.write(
                f"Customer: **{customer_name}**"
            )

            st.write(
                f"Total Paid: **₦{total:,.2f}**"
            )


            st.write("📦 Items:")

            for item in cart:

                st.write(
                    f"- {item['name']} "
                    f"x {item['quantity']}"
                )


            clear_cart()


            st.button(
                "🛍 Continue Shopping"
            )


        else:

            st.error(
                f"Failed to place order.\n\n{result}"
            )