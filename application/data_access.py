import mysql.connector


def connect_to_database():
    host = "localhost"
    user = "root"
    password = ""
    database = "product_db"

    try:
        conn = mysql.connector.connect(
            host=host,
            user=user,
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


def create_insert_product_stored_procedure():
    if not check_insert_product_stored_procedure():
        conn = connect_to_database()
        if conn is None:
            return False

        try:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE PROCEDURE insertProduct(
                    IN productName VARCHAR(55),
                    IN productDescription TEXT,
                    IN productPrice FLOAT
                )
                BEGIN
                    INSERT INTO product(productName, productDescription, productPrice)
                    VALUES(productName, productDescription, productPrice);
                END
            """)
            return True
        except mysql.connector.Error as e:
            print(f"Error creating stored procedure: {e}")
            return False
        finally:
            cursor.close()
            conn.close()
    else:
        print("Stored procedure insertProduct already exists.")
        return True


# Create the stored procedure if it doesn't exist
create_insert_product_stored_procedure()
