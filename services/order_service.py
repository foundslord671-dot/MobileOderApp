from database.connection import get_connection


def create_order(
    vendor_id,
    customer_name,
    customer_phone,
    customer_address,
    cart
):
    conn = get_connection()
    cur = conn.cursor()

    try:

        total_amount = sum(
            item["price"] * item["quantity"]
            for item in cart
        )

        cur.execute(
            """
            INSERT INTO orders
            (
                vendor_id,
                customer_name,
                customer_phone,
                customer_address,
                total_amount
            )
            VALUES (%s, %s, %s, %s, %s)
            RETURNING id
            """,
            (
                vendor_id,
                customer_name,
                customer_phone,
                customer_address,
                total_amount
            )
        )

        order_id = cur.fetchone()[0]

        for item in cart:

            cur.execute(
                """
                INSERT INTO order_items
                (
                    order_id,
                    product_id,
                    quantity,
                    price
                )
                VALUES (%s, %s, %s, %s)
                """,
                (
                    order_id,
                    item["id"],
                    item["quantity"],
                    item["price"]
                )
            )

        conn.commit()

        return True, order_id

    except Exception as e:

        conn.rollback()

        return False, str(e)

    finally:

        cur.close()
        conn.close()


def get_vendor_orders(vendor_id):

    conn = get_connection()
    cur = conn.cursor()

    try:

        cur.execute(
            """
            SELECT
                id,
                customer_name,
                customer_phone,
                customer_address,
                total_amount,
                status,
                created_at
            FROM orders
            WHERE vendor_id = %s
            ORDER BY created_at DESC
            """,
            (vendor_id,)
        )

        return cur.fetchall()

    except Exception:

        return []

    finally:

        cur.close()
        conn.close()


def update_order_status(order_id, vendor_id, status):

    conn = get_connection()
    cur = conn.cursor()

    try:

        cur.execute(
            """
            UPDATE orders
            SET status = %s
            WHERE id = %s
            AND vendor_id = %s
            """,
            (
                status,
                order_id,
                vendor_id
            )
        )

        conn.commit()

        return True

    except Exception:

        conn.rollback()

        return False

    finally:

        cur.close()
        conn.close()


def get_order_items(order_id):

    conn = get_connection()
    cur = conn.cursor()

    try:

        cur.execute(
            """
            SELECT
                products.product_name,
                order_items.quantity,
                order_items.price
            FROM order_items

            JOIN products
            ON order_items.product_id = products.id

            WHERE order_items.order_id = %s
            """,
            (order_id,)
        )

        return cur.fetchall()

    except Exception:

        return []

    finally:

        cur.close()
        conn.close()


# ==========================
# Vendor Analytics
# ==========================

def get_vendor_statistics(vendor_id):

    conn = get_connection()
    cur = conn.cursor()

    try:

        cur.execute(
            """
            SELECT COUNT(*)
            FROM orders
            WHERE vendor_id = %s
            """,
            (vendor_id,)
        )
        total_orders = cur.fetchone()[0]

        cur.execute(
            """
            SELECT
                COALESCE(SUM(total_amount), 0)
            FROM orders
            WHERE vendor_id = %s
            AND status != 'Cancelled'
            """,
            (vendor_id,)
        )
        total_revenue = cur.fetchone()[0]

        cur.execute(
            """
            SELECT COUNT(*)
            FROM products
            WHERE vendor_id = %s
            """,
            (vendor_id,)
        )
        total_products = cur.fetchone()[0]

        return (
            total_orders,
            total_revenue,
            total_products
        )

    except Exception:

        return (
            0,
            0,
            0
        )

    finally:

        cur.close()
        conn.close()


def get_recent_vendor_orders(vendor_id, limit=5):

    conn = get_connection()
    cur = conn.cursor()

    try:

        cur.execute(
            """
            SELECT
                customer_name,
                total_amount,
                status,
                created_at

            FROM orders

            WHERE vendor_id = %s

            ORDER BY created_at DESC

            LIMIT %s
            """,
            (
                vendor_id,
                limit
            )
        )

        return cur.fetchall()

    except Exception:

        return []

    finally:

        cur.close()
        conn.close()