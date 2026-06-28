import streamlit as st

from services.auth_service import login_vendor


st.set_page_config(
    page_title="Login",
    page_icon="🔑"
)


st.title("🔑 Login")

st.write("Sign in to access your account.")


st.divider()


email = st.text_input("Email Address")

password = st.text_input(
    "Password",
    type="password"
)


st.divider()


if st.button(
    "Login",
    use_container_width=True
):

    if not email:

        st.error("Please enter your email.")


    elif not password:

        st.error("Please enter your password.")


    else:

        success, result = login_vendor(
            email,
            password
        )


        if success:

            st.session_state["logged_in"] = True

            st.session_state["vendor"] = result


            st.success(
                "✅ Login successful!"
            )


            if result["is_admin"]:

                st.switch_page(
                    "pages/admin_dashboard.py"
                )

            else:

                st.switch_page(
                    "pages/vendor_dashboard.py"
                )


        else:

            st.error(result)