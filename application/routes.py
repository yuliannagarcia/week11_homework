from flask import render_template, url_for, request, redirect, session
from application import app
from application.data_access import connect_to_database


# from datetime import datetime
# import os

@app.route('/')
@app.route('/home')
def home():
    products = get_products()
    return render_template('index.html', products=products)


@app.route('/add_to_basket/<int:product_id>')
def add_to_basket(product_id):
    session.setdefault('basket', [])
    session['basket'].append(product_id)

    return redirect(url_for('product_list'))


@app.route('/basket')
def view_basket():
    basket = session.get('basket', [])
    return render_template('basket.html', basket=basket)


@app.route('/remove_from_basket/<int:product_id>')
def remove_from_basket(product_id):
    basket = session.get('basket', [])
    if product_id in basket:
        basket.remove(product_id)
        session['basket'] = basket
    return redirect(url_for('view_basket'))


@app.route('/add_product', methods=['POST'])
def add_product_route():
    name = request.form['name']
    description = request.form['description']
    price = request.form['price']
    add_product(name, description, price)
    return redirect('/')


@app.route('/get_products')
def get_products():
    conn = connect_to_database()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM product")
    products = cursor.fetchall()
    cursor.close()
    conn.close()
    return products


def add_product(productName, productDescription, productPrice):
    conn = connect_to_database()
    cursor = conn.cursor()
    # cursor.execute("call procedure insertProduct('wallet', 'LV', '49.99')",
    #                (productName, productDescription, productPrice))
    cursor.callproc("insertProduct", [productName, productDescription, productPrice])
    conn.commit()
    cursor.close()
    conn.close()
