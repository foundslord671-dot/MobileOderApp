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


# -----------------------------
# GET CART
# -----------------------------
cart = get_cart()


# -----------------------------
# EMPTY CART CHECK
# -----------------------------
if not cart:
    st.info("Your cart is empty.")
    st.stop()


# -----------------------------
# CONTINUE SHOPPING BUTTON
# -----------------------------
if "current_store" in st.session_state:
    if st.button("⬅ Continue Shopping"):
        st.query_params["store"] = st.session_state["current_store"]
        st.rerun()


st.divider()


# -----------------------------
# CART ITEMS
# -----------------------------
for item in cart:

    with st.container(border=True):

        st.subheader(item.get("name", "Unnamed Item"))

        st.write(f"Price: ₦{item.get('price', 0):,.2f}")
        st.write(f"Quantity: {item.get('quantity', 1)}")

        subtotal = item.get("price", 0) * item.get("quantity", 1)
        st.write(f"Subtotal: ₦{subtotal:,.2f}")

        if st.button("🗑 Remove", key=f"remove_{item['id']}"):
            remove_from_cart(item["id"])
            st.rerun()


st.divider()


# -----------------------------
# TOTAL + CLEAR CART
# -----------------------------
total = get_cart_total()

col1, col2 = st.columns([3, 1])

with col1:
    st.subheader(f"Total: ₦{total:,.2f}")

with col2:
    if st.button("🗑 Clear Cart"):
        clear_cart()
        st.success("Cart cleared.")
        st.rerun()


st.divider()


# -----------------------------
# CUSTOMER INFO
# -----------------------------
st.subheader("Customer Information")

customer_name = st.text_input("Full Name")
customer_phone = st.text_input("Phone Number")
customer_address = st.text_area("Delivery Address")


# -----------------------------
# CHECKOUT
# -----------------------------
if st.button("✅ Place Order", use_container_width=True):

    if not customer_name.strip() or not customer_phone.strip() or not customer_address.strip():
        st.error("Please fill in all customer information.")
        st.stop()

    # -----------------------------
    # SAFE VENDOR CHECK
    # -----------------------------
    vendor_ids = [item.get("vendor_id") for item in cart]

    if any(v is None for v in vendor_ids):
        st.error("This cart contains invalid items. Please clear cart and try again.")
        st.stop()

    if len(set(vendor_ids)) > 1:
        st.error("You cannot order from multiple vendors at once.")
        st.stop()

    vendor_id = vendor_ids[0]


    # -----------------------------
    # CREATE ORDER
    # -----------------------------
    success, result = create_order(
        vendor_id,
        customer_name.strip(),
        customer_phone.strip(),
        customer_address.strip(),
        cart
    )

    if success:

        order_number = result

        st.success("🎉 Order placed successfully!")
        st.balloons()

        st.subheader("🧾 Order Summary")
        st.write(f"Order Number: #{order_number}")
        st.write(f"Customer: {customer_name}")
        st.write(f"Total: ₦{total:,.2f}")

        st.write("Items:")

        for item in cart:
            st.write(f"• {item['name']} × {item['quantity']}")

        clear_cart()

    else:
        st.error(result)