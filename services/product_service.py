from database.connection import get_connection


def add_product(vendor_id, product_name, description, price, stock, image_url=None):

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        INSERT INTO products
        (vendor_id, product_name, description, price, stock, image_url)
        VALUES (%s, %s, %s, %s, %s, %s)
        """,
        (
            vendor_id,
            product_name,
            description,
            price,
            stock,
            image_url
        )
    )

    conn.commit()

    cur.close()
    conn.close()



def get_vendor_products(vendor_id):

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        SELECT id, product_name, description, price, stock, image_url
        FROM products
        WHERE vendor_id = %s
        ORDER BY created_at DESC
        """,
        (vendor_id,)
    )

    products = cur.fetchall()

    cur.close()
    conn.close()

    return products



def get_all_products():

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        SELECT
            products.id,
            products.product_name,
            products.description,
            products.price,
            products.stock,
            products.image_url,
            vendors.business_name,
            vendors.store_username,
            vendors.phone

        FROM products

        JOIN vendors

        ON products.vendor_id = vendors.id

        ORDER BY products.created_at DESC
        """
    )

    products = cur.fetchall()

    cur.close()
    conn.close()

    return products



def delete_product(product_id, vendor_id):

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        DELETE FROM products
        WHERE id = %s
        AND vendor_id = %s
        """,
        (
            product_id,
            vendor_id
        )
    )

    conn.commit()

    cur.close()
    conn.close()



def update_product(
    product_id,
    vendor_id,
    product_name,
    description,
    price,
    stock
):

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        UPDATE products

        SET
            product_name = %s,
            description = %s,
            price = %s,
            stock = %s

        WHERE id = %s
        AND vendor_id = %s
        """,
        (
            product_name,
            description,
            price,
            stock,
            product_id,
            vendor_id
        )
    )

    conn.commit()

    cur.close()
    conn.close()



def get_product_statistics(vendor_id):

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        SELECT
            COUNT(*),
            COALESCE(SUM(stock),0),
            COALESCE(SUM(price * stock),0)

        FROM products

        WHERE vendor_id = %s
        """,
        (vendor_id,)
    )

    stats = cur.fetchone()

    cur.close()
    conn.close()

    return stats



# =====================================
# Reviews & Ratings
# =====================================


def add_review(
    product_id,
    vendor_id,
    customer_name,
    rating,
    review
):

    conn = get_connection()
    cur = conn.cursor()

    try:

        cur.execute(
            """
            INSERT INTO reviews
            (
                product_id,
                vendor_id,
                customer_name,
                rating,
                review
            )

            VALUES (%s,%s,%s,%s,%s)
            """,
            (
                product_id,
                vendor_id,
                customer_name,
                rating,
                review
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



def get_product_reviews(product_id):

    conn = get_connection()
    cur = conn.cursor()

    try:

        cur.execute(
            """
            SELECT
                customer_name,
                rating,
                review,
                created_at

            FROM reviews

            WHERE product_id = %s

            ORDER BY created_at DESC
            """,
            (product_id,)
        )

        return cur.fetchall()


    except Exception:

        return []


    finally:

        cur.close()
        conn.close()



def get_product_rating(product_id):

    conn = get_connection()
    cur = conn.cursor()

    try:

        cur.execute(
            """
            SELECT
                COALESCE(AVG(rating),0),
                COUNT(*)

            FROM reviews

            WHERE product_id = %s
            """,
            (product_id,)
        )

        return cur.fetchone()


    except Exception:

        return (0,0)


    finally:

        cur.close()
        conn.close()



# =====================================
# Product Search
# =====================================


def search_products(keyword):

    conn = get_connection()
    cur = conn.cursor()

    try:

        search = f"%{keyword}%"

        cur.execute(
            """
            SELECT
                products.id,
                products.product_name,
                products.description,
                products.price,
                products.stock,
                products.image_url,
                vendors.business_name,
                vendors.store_username,
                vendors.phone

            FROM products

            JOIN vendors

            ON products.vendor_id = vendors.id

            WHERE
                products.product_name ILIKE %s

                OR products.description ILIKE %s

                OR vendors.business_name ILIKE %s

            ORDER BY products.created_at DESC
            """,
            (
                search,
                search,
                search
            )
        )

        return cur.fetchall()


    except Exception:

        return []


    finally:

        cur.close()
        conn.close()