import pandas as pd
import numpy as np
from flask import Flask, render_template, request

app = Flask(__name__)

stall_phone_number = None

item_prices = {
    'Steamed Chicken Rice': 5.00,
    'Whole Steamed Chicken': 20.00,
    'Half Steamed Chicken': 15.00
}

@app.route('/')
def login():
    return render_template('login.html')

# add python code for home below
@app.route('/home')
def home():
    return render_template('customer_home.html')


# here is where the ngas can see what they ordered
@app.route('/checkout', methods=['GET', 'POST']) # Maybe add a msg as well to say 'u hvnt ordered shi', but not yet focus on basics first
def checkout():
    if request.method == 'POST':
        items_ordered = request.form.getlist('items')
        print(items_ordered)
        price_list = []
        total_cost = 0
        for item in items_ordered:
            item_price = item_prices[item]
            price_list.append(item_price)
            total_cost += item_price
        return render_template('checkout.html', items_ordered = items_ordered, price_list = price_list, total_cost = total_cost)
    else:
        return render_template('customer_home.html')


# here is where they scan the qr code and submit ss of paynow
@app.route('/payment', methods=['POST'])
def payment():
    payment_amount = request.form.getlist('items')
    return render_template('payment.html', payment_amount = payment_amount)
    #STOPPPED HEREEE

# this is where the YOLO will take out all the impt info and verify, as well as upload the data to a database
@app.route('/confirmation', methods=['POST'])
def confirmation():
    return render_template('confirmation.html')

# do stall owner stuff only after u finish all the customer stuff
@app.route('/admin_home', methods=['POST'])
def admin_home():
    return render_template('admin_home.html')





if __name__ == "__main__":
    app.run(debug=True)