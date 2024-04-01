from flask import render_template, url_for, request, redirect, session
from application import app


# from datetime import datetime
# import os

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
