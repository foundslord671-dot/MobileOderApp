import streamlit as st


def initialize_cart():
    """Create the shopping cart if it doesn't exist."""
    if "cart" not in st.session_state:
        st.session_state.cart = []


def add_to_cart(product):
    """Add a product to the cart."""

    initialize_cart()

    # Check if product already exists
    for item in st.session_state.cart:
        if item["id"] == product["id"]:
            item["quantity"] += 1
            return

    product["quantity"] = 1
    st.session_state.cart.append(product)


def remove_from_cart(product_id):
    """Remove a product from the cart."""

    initialize_cart()

    st.session_state.cart = [
        item
        for item in st.session_state.cart
        if item["id"] != product_id
    ]


def clear_cart():
    """Remove every product from the cart."""

    st.session_state.cart = []


def get_cart():
    """Return all products currently in the cart."""

    initialize_cart()

    return st.session_state.cart


def get_cart_total():
    """Calculate the total price."""

    initialize_cart()

    total = 0

    for item in st.session_state.cart:
        total += item["price"] * item["quantity"]

    return total