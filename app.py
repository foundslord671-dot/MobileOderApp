import streamlit as st

# -----------------------------
# SESSION STATE INITIALIZATION
# -----------------------------
if "cart" not in st.session_state:
    st.session_state.cart = []

if "page" not in st.session_state:
    st.session_state.page = "store"


# -----------------------------
# SAMPLE PRODUCTS
# -----------------------------
products = [
    {"id": 1, "name": "Phone", "price": 50000},
    {"id": 2, "name": "Laptop", "price": 350000},
    {"id": 3, "name": "Headphones", "price": 15000},
    {"id": 4, "name": "Shoes", "price": 20000},
]


# -----------------------------
# FUNCTIONS
# -----------------------------
def add_to_cart(product):
    for item in st.session_state.cart:
        if item["id"] == product["id"]:
            item["qty"] += 1
            return
    st.session_state.cart.append({"id": product["id"], "name": product["name"], "price": product["price"], "qty": 1})


def cart_total():
    return sum(item["price"] * item["qty"] for item in st.session_state.cart)


# -----------------------------
# STORE PAGE
# -----------------------------
def store_page():
    st.title("🛍️ Store")

    st.button("Go to Cart 🛒", on_click=lambda: set_page("cart"))

    st.write("---")

    for product in products:
        st.subheader(product["name"])
        st.write(f"Price: ₦{product['price']}")

        if st.button(f"Add {product['name']} to cart", key=product["id"]):
            add_to_cart(product)
            st.success("Added to cart!")


# -----------------------------
# CART PAGE
# -----------------------------
def cart_page():
    st.title("🛒 Your Cart")

    if st.button("⬅ Back to Store"):
        set_page("store")

    st.write("---")

    if len(st.session_state.cart) == 0:
        st.info("Your cart is empty.")
        return

    for item in st.session_state.cart:
        st.write(f"{item['name']} x{item['qty']} = ₦{item['price'] * item['qty']}")

    st.write("---")
    st.subheader(f"Total: ₦{cart_total()}")


# -----------------------------
# PAGE CONTROLLER
# -----------------------------
def set_page(page):
    st.session_state.page = page
    st.rerun()


# -----------------------------
# ROUTING
# -----------------------------
if st.session_state.page == "store":
    store_page()
elif st.session_state.page == "cart":
    cart_page()