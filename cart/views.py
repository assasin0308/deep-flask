from flask import render_template
from . import app_cart

@app_cart.route('/get_cart')
def get_cart():
    return render_template('cart.html')
