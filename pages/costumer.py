import streamlit as st
import urllib.parse

from services.product_service import get_all_products


st.set_page_config(
    page_title="Customer Store",
    page_icon="🛒",
    layout="wide"
)


st.title("🛒 Customer Store")

st.write("Browse products from different vendors.")


st.divider()


products = get_all_products()


search = st.text_input(
    "🔍 Search products"
)


if search:
    products = [
        product
        for product in products
        if search.lower() in product[1].lower()
    ]


if not products:

    st.info("No products available.")

else:

    cols = st.columns(3)

    for index, product in enumerate(products):

        product_id = product[0]
        product_name = product[1]
        description = product[2]
        price = product[3]
        stock = product[4]
        image_url = product[5]
        business_name = product[6]
        store_username = product[7]
        vendor_phone = product[8]


        with cols[index % 3]:

            with st.container(border=True):

                if image_url:
                    st.image(
                        image_url,
                        use_container_width=True
                    )


                st.subheader(product_name)

                if description:
                    st.write(description)


                st.write(f"💰 Price: ₦{price}")
                st.write(f"📦 Stock: {stock}")
                st.write(f"🏪 Vendor: {business_name}")


                message = (
                    f"Hello, I want to order {product_name}."
                    f"\nPrice: ₦{price}"
                )


                whatsapp_message = urllib.parse.quote(message)


                whatsapp_link = (
                    f"https://wa.me/{vendor_phone}"
                    f"?text={whatsapp_message}"
                )


                st.link_button(
                    "📱 Order on WhatsApp",
                    whatsapp_link,
                    use_container_width=True
                )