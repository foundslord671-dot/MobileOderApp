import streamlit as st

from components.admin_sidebar import show_admin_sidebar

from services.admin_service import (
    get_all_vendors,
    update_vendor_status
)


st.set_page_config(
    page_title="Manage Vendors",
    page_icon="👥",
    layout="wide"
)


# Protect page
if "logged_in" not in st.session_state or not st.session_state["logged_in"]:
    st.warning("Please log in first.")
    st.switch_page("pages/login.py")


user = st.session_state["vendor"]


# Check admin access
if not user["is_admin"]:
    st.error("Access denied. Admins only.")
    st.stop()


# Show admin sidebar
show_admin_sidebar()



st.title("👥 Manage Vendors")


vendors = get_all_vendors()


if not vendors:

    st.info("No vendors found.")


else:

    st.success(
        f"{len(vendors)} vendor(s) found."
    )


    st.divider()


    for vendor in vendors:

        vendor_id = vendor[0]
        business_name = vendor[1]
        owner_name = vendor[2]
        email = vendor[3]
        phone = vendor[4]
        store_username = vendor[5]
        is_active = vendor[6]


        with st.container(border=True):

            st.subheader(business_name)


            st.write(
                f"👤 Owner: {owner_name}"
            )

            st.write(
                f"📧 Email: {email}"
            )

            st.write(
                f"📞 Phone: {phone}"
            )

            st.write(
                f"🏷 Store: {store_username}"
            )


            status = "Active ✅" if is_active else "Disabled ❌"

            st.write(
                f"Status: {status}"
            )


            if is_active:

                if st.button(
                    "❌ Disable Vendor",
                    key=f"disable_{vendor_id}"
                ):

                    update_vendor_status(
                        vendor_id,
                        False
                    )

                    st.rerun()


            else:

                if st.button(
                    "✅ Activate Vendor",
                    key=f"activate_{vendor_id}"
                ):

                    update_vendor_status(
                        vendor_id,
                        True
                    )

                    st.rerun()