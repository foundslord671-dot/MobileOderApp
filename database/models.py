from database.connection import get_connection


def create_tables():
    conn = get_connection()
    cur = conn.cursor()

    # Vendors table
    cur.execute("""
    CREATE TABLE IF NOT EXISTS vendors (
        id SERIAL PRIMARY KEY,

        business_name VARCHAR(150) NOT NULL,
        owner_name VARCHAR(150) NOT NULL,

        store_username VARCHAR(50) UNIQUE NOT NULL,

        email VARCHAR(255) UNIQUE NOT NULL,
        phone VARCHAR(20),

        password_hash TEXT NOT NULL,

        is_admin BOOLEAN DEFAULT FALSE,
        is_active BOOLEAN DEFAULT TRUE,

        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)

    # Products table
    cur.execute("""
    CREATE TABLE IF NOT EXISTS products (
        id SERIAL PRIMARY KEY,

        vendor_id INTEGER NOT NULL REFERENCES vendors(id) ON DELETE CASCADE,

        product_name VARCHAR(200) NOT NULL,
        description TEXT,

        price NUMERIC(12,2) NOT NULL,
        stock INTEGER DEFAULT 0,

        image_url TEXT,

        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)

    # Orders table
    cur.execute("""
    CREATE TABLE IF NOT EXISTS orders (
        id SERIAL PRIMARY KEY,

        vendor_id INTEGER NOT NULL REFERENCES vendors(id) ON DELETE CASCADE,

        customer_name VARCHAR(150) NOT NULL,
        customer_phone VARCHAR(20) NOT NULL,
        customer_address TEXT NOT NULL,

        total_amount NUMERIC(12,2) NOT NULL,

        status VARCHAR(30) DEFAULT 'Pending',

        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)

    # Order Items table
    cur.execute("""
    CREATE TABLE IF NOT EXISTS order_items (
        id SERIAL PRIMARY KEY,

        order_id INTEGER NOT NULL REFERENCES orders(id) ON DELETE CASCADE,

        product_id INTEGER NOT NULL REFERENCES products(id),

        quantity INTEGER NOT NULL,

        price NUMERIC(12,2) NOT NULL
    );
    """)

    # Reviews table
    cur.execute("""
    CREATE TABLE IF NOT EXISTS reviews (
        id SERIAL PRIMARY KEY,

        product_id INTEGER NOT NULL REFERENCES products(id) ON DELETE CASCADE,

        vendor_id INTEGER NOT NULL REFERENCES vendors(id) ON DELETE CASCADE,

        customer_name VARCHAR(150) NOT NULL,

        rating INTEGER NOT NULL CHECK (rating BETWEEN 1 AND 5),

        review TEXT,

        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)

    conn.commit()

    cur.close()
    conn.close()