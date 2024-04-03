import mysql.connector
import platform


def connect_to_database():
    # Determine the operating system
    system = platform.system()

    # Set default values
    host = "localhost"
    user = "root"
    password = ""
    database = "product_db"

    # Override default values based on the operating system
    if system == 'Windows':
        host = "localhost"
        user = "root"
        password = "password"
        database = "product_db"
    # elif system == 'Linux':
    #     host = "linux_host"
    #     user = "linux_user"
    #     password = "linux_password"
    #     database = "linux_database"
    elif system == 'Darwin':  # macOS
        host = "localhost"
        user = "root"
        password = ""
        database = "product_db"

    try:
        conn = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        return conn
    except mysql.connector.Error as e:
        print(f"Error connecting to MySQL database: {e}")
        return None


def get_products():
    conn = connect_to_database()
    if conn is None:
        return []

    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM product")
        products = cursor.fetchall()
        return products
    except mysql.connector.Error as e:
        print(f"Error executing query: {e}")
        return []
    finally:
        if 'cursor' in locals():
            cursor.close()
        conn.close()


def add_product_to_database(name, description, price):
    conn = connect_to_database()
    if conn is None:
        return False

    try:
        cursor = conn.cursor()
        cursor.callproc("insertProduct", [name, description, price])
        conn.commit()
        return True
    except mysql.connector.Error as e:
        print(f"Error executing query: {e}")
        return False
    finally:
        cursor.close()
        conn.close()


def remove_product_from_database(product_id):
    conn = connect_to_database()
    if conn is None:
        return False

    try:
        cursor = conn.cursor()
        cursor.callproc("removeProduct", [product_id])
        conn.commit()
        return True
    except mysql.connector.Error as e:
        print(f"Error executing query: {e}")
        return False
    finally:
        cursor.close()
        conn.close()


def check_insert_product_stored_procedure():
    conn = connect_to_database()
    if conn is None:
        return False

    try:
        cursor = conn.cursor()
        cursor.execute("SHOW PROCEDURE STATUS WHERE Db = 'product_db' AND Name = 'insertProduct'")
        result = cursor.fetchone()
        return result is not None
    except mysql.connector.Error as e:
        print(f"Error checking stored procedure existence: {e}")
        return False
    finally:
        cursor.close()
        conn.close()
