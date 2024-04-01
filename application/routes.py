# from flask import render_template, url_for, request, redirect, session, jsonify
# from application import app
# from application.data_access import add_product_to_database, get_product_by_id, get_products
#
#
# @app.route('/')
# def home():
#     products_ = get_products()  # Fetch products from the database
#     return render_template('index.html', products=products_)
#
#
# @app.route('/add_to_basket/<int:product_id>', methods=['GET', 'POST'])
# def add_or_view_basket(product_id):
#     if request.method == 'POST':
#         # Handle POST request to add product to basket
#         session.setdefault('basket', [])
#         quantity = int(request.form['quantity'])  # Retrieve quantity from form data
#         session['basket'].append({'product_id': product_id, 'quantity': quantity})
#         return redirect(url_for('view_basket'))
#     else:
#         # If the request is GET, redirect to view basket directly
#         return redirect(url_for('view_basket'))
#
#
# @app.route('/add_to_basket/<int:product_id>', methods=['POST'])
# def add_to_basket(product_id):
#     if request.method == 'POST':
#         # Handle POST request to add product to basket
#         session.setdefault('basket', [])
#         quantity = int(request.form['quantity'])  # Retrieve quantity from form data
#         session['basket'].append({'product_id': product_id, 'quantity': quantity})
#         return redirect(url_for('view_basket'))
#     else:
#         # If the request is GET, redirect to view basket directly
#         return redirect(url_for('view_basket'))
#
#
# @app.route('/basket')
# def view_basket():
#     basket = session.get('basket', [])
#
#     # Retrieve details of products in the basket from the database
#     products_in_basket = []
#     total_price = 0
#     for item in basket:
#         product = get_product_by_id(item['product_id'])
#         if product:
#             products_in_basket.append({
#                 'name': product['ProductName'],
#                 'description': product['ProductDescription'],
#                 'price': product['ProductPrice'],
#                 'quantity': item['quantity']
#             })
#             total_price += product['ProductPrice'] * item['quantity']
#
#     return render_template('basket.html', products=products_in_basket, total_price=total_price)
#
#
# @app.route('/add_product', methods=['POST'])
# def add_product():
#     name = request.form['name']
#     description = request.form['description']
#     price = float(request.form['price'])  # Convert price to float
#     add_product_to_database(name, description, price)
#     return redirect(url_for('home'))
#
#
# @app.route('/print_products_and_prices')
# def print_products_and_prices():
#     # Fetch products from the database
#     products = get_products()
#
#     # Create a dictionary to store product names and prices
#     products_and_prices = {}
#
#     # Iterate through the products and populate the dictionary
#     for product in products:
#         products_and_prices[product['ProductName']] = product['ProductPrice']
#
#     # Return the dictionary as JSON response
#     return jsonify(products_and_prices)

from flask import render_template, url_for, request, redirect, session, jsonify
from application import app
from application.data_access import add_product_to_database, get_product_by_id, get_products


@app.route('/')
def home():
    products = get_products()  # Fetch products from the database
    return render_template('index.html', products=products)


@app.route('/add_to_basket/<int:product_id>', methods=['POST'])
def add_to_basket(product_id):
    if request.method == 'POST':
        # Retrieve quantity from form data
        quantity = int(request.form['quantity'])

        # Initialize basket in session if not already present
        session.setdefault('basket', [])

        # Add product ID and quantity to the basket in session
        session['basket'].append({'product_id': product_id, 'quantity': quantity})

    return redirect(url_for('home'))


# @app.route('/basket')
# def view_basket():
#     basket = session.get('basket', [])
#     total_price = 0
#
#     # Retrieve details of products in the basket from the database
#     products_in_basket = []
#     for item in basket:
#         product = get_product_by_id(item['product_id'])
#         if product and 'name' in product:
#             product_price = float(product['price'])  # Convert price to float
#             products_in_basket.append({
#                 'name': product['name'],
#                 'price': product_price,
#                 'quantity': item['quantity']
#             })
#             total_price += product_price * item['quantity']
#
#     # Debugging output
#     print("Basket:", basket)
#     print("Products in basket:", products_in_basket)
#     print("Total price:", total_price)
#
#     return render_template('basket.html', products=products_in_basket, total_price=total_price)

@app.route('/basket')
def view_basket():
    basket = session.get('basket', [])
    total_price = 0
    products_in_basket = []

    for item in basket:
        product = get_product_by_id(item['product_id'])
        if product:
            total_price += product['ProductPrice'] * item['quantity']
            products_in_basket.append({
                'name': product['ProductName'],
                'description': product['ProductDescription'],
                'price': product['ProductPrice'],
                'quantity': item['quantity']
            })

    return render_template('basket.html', products=products_in_basket, total_price=total_price)


@app.route('/remove_from_basket/<int:product_id>')
def remove_from_basket(product_id):
    basket = session.get('basket', [])
    for item in basket:
        if item['product_id'] == product_id:
            basket.remove(item)
            break
    session['basket'] = basket
    return redirect(url_for('view_basket'))


@app.route('/add_product', methods=['POST'])
def add_product():
    name = request.form['name']
    description = request.form['description']
    price = float(request.form['price'])  # Convert price to float
    add_product_to_database(name, description, price)
    return redirect(url_for('home'))


@app.route('/print_products_and_prices')
def print_products_and_prices():
    # Fetch products from the database
    products = get_products()
<<<<<<< HEAD

    # Create a dictionary to store product names and prices
    products_and_prices = {}

    # Iterate through the products and populate the dictionary
    for product in products:
        products_and_prices[product['ProductName']] = product['ProductPrice']

    # Return the dictionary as JSON response
    return jsonify(products_and_prices)
=======
    total_price = 0
    for item in basket:
        for product in products:
            # if item['product_id'] == product['id']:
            if 'ProductPrice' in product and 'quantity' in item:
                total_price += product['ProductPrice'] * item['quantity']
                break  # Exit the inner loop once the product is found
    return total_price


@app.route('/checkout', methods=['POST'])
def checkout():
    # Clear the session to empty the basket
    session.pop('basket', None)
    # Render the basket template with the thank-you message shown
    return render_template('basket.html', thank_you=True)
>>>>>>> a10bb61d6b2dede8da1995223a1078f9eb2bd22a
