import mysql.connector
from flask import redirect, request, render_template

from application import app

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Pa$$w0rd",
    database="productDB"
)


def get_db_connection():
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Pa$$w0rd",
        database="product_db"
    )
    return mydb


def connect_to_database():
    return mysql.connector.connect(
        host="hostname",
        user="username",
        password="Pa$$w0rd",
        database="product_db"
    )


@app.route('/')
def home():
    products = get_products()
    return render_template('index.html', products=products)


@app.route('/add_product', methods=['POST'])
def add_product_route():
    name = request.form['name']
    description = request.form['description']
    price = request.form['price']
    add_product(name, description, price)
    return redirect('/')


def get_products():
    conn = connect_to_database()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM products")
    products = cursor.fetchall()
    cursor.close()
    conn.close()
    return products


def add_product(name, description, price):
    conn = connect_to_database()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO products (name, description, price) VALUES (%s, %s, %s)", (name, description, price))
    conn.commit()
    cursor.close()
    conn.close()
