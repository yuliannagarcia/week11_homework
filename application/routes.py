from flask import render_template, url_for, request, redirect, session, flash
from application import app
from application.data_access import add_product_to_database, remove_product_from_database
from application.data_access import get_products
from flask import render_template, request



@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')


PRODUCTS_PER_PAGE = 6

@app.route('/index')
def index():
    page = request.args.get('page', 1, type=int)  # Get the page number from the query parameters

    products = get_products()  # Fetch all products from the database

    # Calculate the total number of pages
    products_per_page = 6
    total_pages = (len(products) + products_per_page - 1) // products_per_page

    # Calculate the start and end indices for pagination
    start_index = (page - 1) * products_per_page
    end_index = min(start_index + products_per_page, len(products))

    # Get the products for the current page
    paginated_products = products[start_index:end_index]

    return render_template('index.html', products=paginated_products, total_pages=total_pages, page=page)

@app.route('/add_to_basket/<int:product_id>', methods=['POST'])
def add_to_basket(product_id):
    if request.method == 'POST':
        # Handle POST request to add product to basket
        session.setdefault('basket', [])
        quantity = int(request.form['quantity'])  # Retrieve quantity from form data
        session['basket'].append({'product_id': product_id, 'quantity': quantity})
        session.modified = True  # updating session with latest basket information
    return redirect(url_for('index'))


@app.route('/basket', methods=['GET', 'POST'])
def view_basket():
    basket = session.get('basket', [])
    products = get_products()
    total_price = calculate_total_price(basket)

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


@app.route('/add_product', methods=['POST'])
def add_product():
    name = request.form['name']
    description = request.form['description']
    price = float(request.form['price'])  # Convert price to float
    add_product_to_database(name, description, price)
    return redirect(url_for('home'))


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
