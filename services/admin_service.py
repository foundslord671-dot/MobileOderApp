from database.connection import get_connection



def get_admin_statistics():

    conn = get_connection()
    cur = conn.cursor()

    try:

        cur.execute(
            "SELECT COUNT(*) FROM vendors"
        )
        total_vendors = cur.fetchone()[0]


        cur.execute(
            "SELECT COUNT(*) FROM products"
        )
        total_products = cur.fetchone()[0]


        cur.execute(
            "SELECT COUNT(*) FROM orders"
        )
        total_orders = cur.fetchone()[0]


        return (
            total_vendors,
            total_products,
            total_orders
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





def get_all_vendors():

    conn = get_connection()
    cur = conn.cursor()

    try:

        cur.execute(
            """
            SELECT
                id,
                business_name,
                owner_name,
                email,
                phone,
                store_username,
                is_active
            FROM vendors
            ORDER BY created_at DESC
            """
        )

        return cur.fetchall()


    except Exception:

        return []


    finally:

        cur.close()
        conn.close()





def update_vendor_status(vendor_id, status):

    conn = get_connection()
    cur = conn.cursor()

    try:

        cur.execute(
            """
            UPDATE vendors
            SET is_active = %s
            WHERE id = %s
            """,
            (
                status,
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





def get_all_orders():

    conn = get_connection()
    cur = conn.cursor()

    try:

        cur.execute(
            """
            SELECT
                orders.id,
                vendors.business_name,
                orders.customer_name,
                orders.customer_phone,
                orders.customer_address,
                orders.total_amount,
                orders.status,
                orders.created_at

            FROM orders

            JOIN vendors
            ON orders.vendor_id = vendors.id

            ORDER BY orders.created_at DESC
            """
        )

        return cur.fetchall()


    except Exception:

        return []


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





def update_order_status(order_id, status):

    conn = get_connection()
    cur = conn.cursor()

    try:

        cur.execute(
            """
            UPDATE orders
            SET status = %s
            WHERE id = %s
            """,
            (
                status,
                order_id
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





def get_all_products():

    conn = get_connection()
    cur = conn.cursor()

    try:

        cur.execute(
            """
            SELECT
                products.id,
                products.product_name,
                products.description,
                products.price,
                products.stock,
                vendors.business_name,
                products.created_at

            FROM products

            JOIN vendors
            ON products.vendor_id = vendors.id

            ORDER BY products.created_at DESC
            """
        )

        return cur.fetchall()


    except Exception:

        return []


    finally:

        cur.close()
        conn.close()





def delete_product(product_id):

    conn = get_connection()
    cur = conn.cursor()

    try:

        cur.execute(
            """
            DELETE FROM products
            WHERE id = %s
            """,
            (product_id,)
        )

        conn.commit()

        return True


    except Exception:

        conn.rollback()

        return False


    finally:

        cur.close()
        conn.close()