from database.connection import get_connection


def email_exists(email):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "SELECT id FROM vendors WHERE email = %s",
        (email,)
    )

    result = cur.fetchone()

    cur.close()
    conn.close()

    return result is not None


def create_vendor(
    business_name,
    owner_name,
    email,
    phone,
    password_hash
):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO vendors
        (
            business_name,
            owner_name,
            email,
            phone,
            password_hash
        )
        VALUES (%s, %s, %s, %s, %s)
    """,
    (
        business_name,
        owner_name,
        email,
        phone,
        password_hash
    ))

    conn.commit()

    cur.close()
    conn.close()