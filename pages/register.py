import streamlit as st

from database.connection import get_connection
from utils.security import hash_password
from services.auth_service import login_vendor


st.set_page_config(
    page_title="Vendor Registration",
    page_icon="📝"
)


st.title("📝 Vendor Registration")
st.write("Create your vendor account below.")

st.divider()


business_name = st.text_input("Business Name")
owner_name = st.text_input("Owner Name")
store_username = st.text_input("Store Username")

email = st.text_input("Email Address")
phone = st.text_input("Phone Number")

password = st.text_input(
    "Password",
    type="password"
)

confirm_password = st.text_input(
    "Confirm Password",
    type="password"
)


st.divider()


if st.button("Create Account", use_container_width=True):

    if not business_name:
        st.error("Please enter your business name.")

    elif not owner_name:
        st.error("Please enter your name.")

    elif not store_username:
        st.error("Please choose a store username.")

    elif not email:
        st.error("Please enter your email.")

    elif not phone:
        st.error("Please enter your phone number.")

    elif not password:
        st.error("Please enter a password.")

    elif password != confirm_password:
        st.error("Passwords do not match.")

    else:

        try:

            conn = get_connection()
            cur = conn.cursor()

            # Check existing email
            cur.execute(
                "SELECT id FROM vendors WHERE email = %s",
                (email,)
            )

            email_exists = cur.fetchone()

            # Check existing username
            cur.execute(
                "SELECT id FROM vendors WHERE store_username = %s",
                (store_username,)
            )

            username_exists = cur.fetchone()

            if email_exists:
                st.error("This email is already registered.")

            elif username_exists:
                st.error("This store username is already taken.")

            else:

                password_hash = hash_password(password)

                cur.execute(
                    """
                    INSERT INTO vendors
                    (
                        business_name,
                        owner_name,
                        store_username,
                        email,
                        phone,
                        password_hash
                    )
                    VALUES
                    (%s,%s,%s,%s,%s,%s)
                    """,
                    (
                        business_name,
                        owner_name,
                        store_username,
                        email,
                        phone,
                        password_hash
                    )
                )

                conn.commit()

                cur.close()
                conn.close()

                # Automatically log the user in
                success, result = login_vendor(
                    email,
                    password
                )

                if success:

                    st.session_state["logged_in"] = True
                    st.session_state["vendor"] = result

                    st.success(
                        "✅ Account created successfully!"
                    )

                    st.switch_page(
                        "pages/vendor_dashboard.py"
                    )

                else:

                    st.success(
                        "✅ Account created successfully!"
                    )

                    st.info(
                        "Please login with your new account."
                    )

            if not conn.closed:
                cur.close()
                conn.close()

        except Exception as e:

            st.error("Something went wrong.")
            st.write(e)