from database.connection import get_connection


email = input("Enter the email of the account to make admin: ")


conn = get_connection()
cur = conn.cursor()


cur.execute(
    """
    UPDATE vendors
    SET is_admin = TRUE
    WHERE email = %s
    """,
    (email,)
)


if cur.rowcount == 1:

    print("✅ Account is now an admin.")

else:

    print("❌ Email not found.")


conn.commit()

cur.close()
conn.close()