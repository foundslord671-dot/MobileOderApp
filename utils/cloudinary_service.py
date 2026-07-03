import cloudinary
import cloudinary.uploader
import streamlit as st


# Configure Cloudinary
cloudinary.config(
    cloud_name=st.secrets["CLOUDINARY_CLOUD_NAME"],
    api_key=st.secrets["CLOUDINARY_API_KEY"],
    api_secret=st.secrets["CLOUDINARY_API_SECRET"],
    secure=True
)


def upload_image(image_file):
    """
    Upload an image to Cloudinary.

    Returns:
        str: Secure image URL
        None: If upload fails
    """

    try:
        result = cloudinary.uploader.upload(image_file)

        return result["secure_url"]

    except Exception as e:
        st.error(f"Image upload failed: {e}")
        return None