import mysql.connector

from flask import render_template
from application import app

# @app.route('/')
# @app.route('/home')
# def home():
#     products_ = get_products()  # Fetch products from the database
#     return render_template('index.html', products=products_)

# mydb = mysql.connector.connect(
#     host="localhost",
#     user="root",
#     password="Pa$$w0rd",
#     database="product_db"
# )
#
#
# def get_db_connection():
#     mydb = mysql.connector.connect(
#         host="localhost",
#         user="root",
#         password="Pa$$w0rd",
#         database="product_db"
#     )
#     return mydb


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
        return


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

# def add_product(productName, productDescription, productPrice):
#     conn = connect_to_database()
#     if conn is None:
#         return False  # Return False if connection fails
#
#     try:
#         cursor = conn.cursor()
#         cursor.callproc("insertProduct", [productName, productDescription, productPrice])
#         conn.commit()
#         return True  # Return True if insertion succeeds
#     except mysql.connector.Error as e:
#         print(f"Error executing query: {e}")
#         return False
