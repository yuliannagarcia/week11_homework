from flask import render_template, url_for, request, redirect, session, jsonify
from flask_wtf import form
from application import app
from application.data_access import get_products, check_insert_product_stored_procedure, remove_product_from_database, \
    add_product_to_database
from application.forms.addproductform import AddToBasketForm


# Renders the home.html template when the / or /home endpoint is accessed.
@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')


# Renders the index.html template for displaying products.
@app.route('/index')
def index():
    page = request.args.get('page', 1, type=int)  # Get the page number from the query parameters

    products = get_products()  # Fetches all products from the database

    # Calculate the total number of pages
    products_per_page = 6
    total_pages = (len(products) + products_per_page - 1) // products_per_page

    # Calculate the start and end indices for pagination
    start_index = (page - 1) * products_per_page
    end_index = min(start_index + products_per_page, len(products))

    # Get the products for the current page
    paginated_products = products[start_index:end_index]

    # Passes the paginated products, total pages, and current page number to the template.
    return render_template('index.html', products=paginated_products, total_pages=total_pages, page=page)


# Handles the addition of products to the basket.
@app.route('/add_to_basket/<int:product_id>', methods=['POST'])
def add_to_basket(product_id):
    if request.method == 'POST':
        # Handle POST request to add product to basket
        session.setdefault('basket', [])
        quantity = int(request.form['quantity'])  # Retrieve quantity from form data
        session['basket'].append({'product_id': product_id, 'quantity': quantity})
        session.modified = True  # updating session with latest basket information
    return redirect(url_for('index'))


# Renders the basket.html template for viewing the basket.
@app.route('/basket', methods=['GET', 'POST'])
def view_basket():
    # Retrieves the basket and products from the session and database, respectively.
    basket = session.get('basket', [])
    products = get_products()
    total_price = calculate_total_price(basket)

    # If the request is POST:: Adds items to the basket based on user input
    if request.method == 'POST':
        # If the request is POST, it means the user is adding items to the basket
        product_id = int(request.form['product_id'])
        quantity = int(request.form['quantity'])

        # Check if the product is already in the basket
        found = False
        for item in basket:
            if item['product_id'] == product_id:
                item['quantity'] += quantity
                found = True
                break

        # If the product is not in the basket, add it
        if not found:
            basket.append({'product_id': product_id, 'quantity': quantity})

        # Update the session
        session['basket'] = basket

    # Render the basket template
    return render_template('basket.html', basket=basket, products=products, total_price=total_price)


@app.route('/remove_from_basket/<int:product_id>', methods=['POST'])
def remove_from_basket(product_id):
    if request.method == 'POST':
        basket = session.get('basket', [])
        for item in basket:
            if item['product_id'] == product_id:
                # Decrement quantity by 1
                item['quantity'] -= 1
                # If quantity becomes 0, remove the item from the basket
                if item['quantity'] == 0:
                    basket.remove(item)
                break
        session['basket'] = basket
        return redirect(url_for('view_basket'))


@app.route('/admin')
def admin():
    form = AddToBasketForm()  # Create the form object
    return render_template('form.html', form=form)


@app.route('/add_product', methods=['POST'])
def add_product():
    if request.method == 'POST':
        # Extract data from the request
        data = request.json
        name = data.get('name')
        description = data.get('description')
        price = data.get('price')

        # Call the add_product_to_database function
        success = add_product_to_database(name, description, price)

        # Check if the operation was successful
        if success:
            return jsonify({'message': 'Product added successfully.'}), 200
        else:
            return jsonify({'error': 'Failed to add product to the database.'}), 500


@app.route('/remove_product/<int:product_id>', methods=['DELETE'])
def remove_product(product_id):
    success = remove_product_from_database(product_id)
    if success:
        return jsonify({'message': f'Product with ID {product_id} removed successfully.'}), 200
    else:
        return jsonify({'error': 'Failed to remove product.'}), 500


@app.route('/check_insert_product_stored_procedure', methods=['GET'])
def check_stored_procedure():
    exists = check_insert_product_stored_procedure()
    if exists:
        return jsonify({'message': 'Stored procedure insertProduct exists.'}), 200
    else:
        return jsonify({'message': 'Stored procedure insertProduct does not exist.'}), 404


def calculate_total_price(basket):
    products = get_products()
    total_price = 0
    for item in basket:
        for product in products:
            if item['product_id'] == product['id']:
                # if 'ProductPrice' in product and 'quantity' in item:
                total_price += product['ProductPrice'] * item['quantity']
                break  # Exit the inner loop once the product is found
    return total_price


@app.route('/checkout', methods=['POST'])
def checkout():
    # Calculate total price
    basket = session.get('basket', [])
    total_price = calculate_total_price(basket)

    # Clear the session to empty the basket
    session.pop('basket', None)

    # Render the checkout template with the total price
    return render_template('checkout.html', total_price=total_price)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session['username'] = request.form['username']
        session['loggedIn'] = True
        session['role'] = 'admin'  # Assuming role is hardcoded for simplicity
        return redirect(url_for('all_products'))
    return render_template('login.html', title="Login")


@app.route('/logout')
def logout():
    session.pop('username', None)
    session.pop('role', None)
    session['loggedIn'] = False
    return redirect(url_for('all_products'))
