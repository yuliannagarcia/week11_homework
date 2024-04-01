from flask import render_template, url_for, request, redirect, session
from application import app
from application.data_access import get_products, add_product_to_database
from application.fakedata import products


@app.route('/')
@app.route('/home')
def home():
    return render_template('index.html', products=products)


# @app.route('/add_to_basket/<int:product_id>', methods=['POST'])
# def add_to_basket(product_id):
#     if request.method == 'POST':
#         # Handle POST request to add product to basket
#         session.setdefault('basket', [])
#         session['basket'].append(product_id)
#     return redirect(url_for('home'))

@app.route('/add_to_basket/<int:product_id>', methods=['POST'])
def add_to_basket(product_id):
    if request.method == 'POST':
        # Handle POST request to add product to basket
        session.setdefault('basket', [])
        quantity = int(request.form['quantity'])  # Retrieve quantity from form data
        session['basket'].append({'product_id': product_id, 'quantity': quantity})
    return redirect(url_for('home'))



@app.route('/basket', methods=['GET', 'POST'])
def view_basket():
    if request.method == 'POST':
        # If the request is POST, it means the user is adding items to the basket
        product_id = int(request.form['product_id'])
        quantity = int(request.form['quantity'])

        # Retrieve or create the basket in the session
        basket = session.get('basket', [])

        # Add the product to the basket
        basket.append({'product_id': product_id, 'quantity': quantity})

        # Update the session
        session['basket'] = basket

        # Render the basket template
        total_price = calculate_total_price(basket)
        return render_template('basket.html', basket=basket, products=products, total_price=total_price)
    else:
        # If the request is GET, it means the user is viewing the basket
        basket = session.get('basket', [])
        total_price = calculate_total_price(basket)
        return render_template('basket.html', basket=basket, products=products, total_price=total_price)


@app.route('/remove_from_basket/<int:product_id>')
def remove_from_basket(product_id):
    basket = session.get('basket', [])
    if product_id in basket:
        basket.remove(product_id)
        session['basket'] = basket
    return redirect(url_for('view_basket'))


@app.route('/add_product', methods=['POST'])
def add_product():
    name = request.form['name']
    description = request.form['description']
    price = float(request.form['price'])  # Convert price to float
    add_product_to_database(name, description, price)
    return redirect(url_for('home'))


def calculate_total_price(basket):
    total_price = 0
    for item in basket:
        for product in products:
            if item['product_id'] == product['id']:
                total_price += product['price'] * item['quantity']
                break  # Exit the inner loop once the product is found
    return total_price
