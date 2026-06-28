from database.connection import get_connection
from utils.security import verify_password


def login_vendor(email, password):
    """
    Authenticate a vendor or admin using email and password.
    Returns (True, user_data) if successful.
    Returns (False, error_message) if not.
    """

    try:
        conn = get_connection()
        cur = conn.cursor()

        cur.execute("""
            SELECT
                id,
                business_name,
                owner_name,
                store_username,
                email,
                password_hash,
                is_active,
                is_admin
            FROM vendors
            WHERE email = %s
        """, (email,))

        vendor = cur.fetchone()

        cur.close()
        conn.close()


        if vendor is None:
            return False, "Email not found."


        if not vendor[6]:
            return False, "Your account has been disabled."


        if not verify_password(password, vendor[5]):
            return False, "Incorrect password."


        return True, {
            "id": vendor[0],
            "business_name": vendor[1],
            "owner_name": vendor[2],
            "store_username": vendor[3],
            "email": vendor[4],
            "is_admin": vendor[7]
        }


    except Exception as e:
        return False, str(e)



def get_vendor_by_username(store_username):

    try:

        conn = get_connection()
        cur = conn.cursor()

        cur.execute("""
            SELECT
                id,
                business_name,
                owner_name,
                store_username,
                phone
            FROM vendors
            WHERE store_username = %s
        """, (store_username,))


        vendor = cur.fetchone()

        cur.close()
        conn.close()

        return vendor


    except Exception:

        return None