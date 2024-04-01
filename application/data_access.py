# import mysql.connector
# from flask import redirect, request, render_template
# from application import routes
#
# from application import app
#
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
#
#
# def connect_to_database():
#     return mysql.connector.connect(
#         host="hostname",
#         user="username",
#         password="Pa$$w0rd",
#         database="product_db"
#     )
#

import mysql.connector
from . import app


def connect_to_database():
    # Replace these placeholders with actual database connection details
    host = "localhost"
    user = "root"
    password = "Pa$$w0rd"
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
        return []  # Return an empty list if connection fails

    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM product")  # Corrected table name to "product"
        products = cursor.fetchall()
        return products
    except mysql.connector.Error as e:
        print(f"Error executing query: {e}")
        return []


def add_product(productName, productDescription, productPrice):
    conn = connect_to_database()
    if conn is None:
        return False  # Return False if connection fails

    try:
        cursor = conn.cursor()
        cursor.callproc("insertProduct", [productName, productDescription, productPrice])
        conn.commit()
        return True  # Return True if insertion succeeds
    except mysql.connector.Error as e:
        print(f"Error executing query: {e}")
        return False


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
