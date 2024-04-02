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


# This function connects to the database using the connect_to_database() function and retrieves all products from the
# product table.It returns a list of dictionaries representing the products.If an error occurs during the execution
# of the query, it prints an error message and returns an empty list.
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


#  This function connects to the database, executes a stored procedure named insertProduct, passing the provided name,
#  description, and price as parameters.If the execution is successful, it commits the transaction and returns True.
#  Otherwise, it prints an error message and returns False.
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


#  This function checks whether the stored procedure named insertProduct exists in the database schema product_db.
#  It executes a SQL query to fetch the procedure's status and returns True if the procedure exists, False otherwise.
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


# This function checks if the insertProduct stored procedure exists. If it does not exist, it attempts to create it
# using a SQL CREATE PROCEDURE statement. If successful, it returns True. If the procedure already exists,
# it prints a message indicating so and returns True. If any errors occur during the creation attempt, it prints an
# error message and returns False.
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
