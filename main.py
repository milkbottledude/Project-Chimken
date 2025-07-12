import pandas as pd
import numpy as np
from flask import Flask, render_template, request
from flask_socketio import SocketIO
import ast
from datetime import datetime, timedelta

app = Flask(__name__)
app.config['SECRET_KEY'] = 'not_the_actual_key'
socketio = SocketIO(app)

stall_phone_number = None

item_prices = {
    'Steamed Chicken Rice': 5.00,
    'Half Steamed Chicken': 15.00,
    'Whole Steamed Chicken': 20.00
}

@app.route('/')
def login():
    return render_template('login.html')

# add python code for home below
@app.route('/old_home')
def home():
    return render_template('customer/customer_home.html')

@app.route('/js_home')
def js_home():
    return render_template('customer/js_customer_home.html')


# here is where the ngas can see what they ordered
@app.route('/checkout', methods=['GET', 'POST']) # Maybe add a msg as well to say 'u hvnt ordered shi', but not yet focus on basics first
def checkout():
    if request.method == 'POST':
        steamed_chicken_rice_ordered = int(request.form.get('SCR_quantity'))
        half_steamed_chicken_ordered = int(request.form.get('HSC_quantity'))
        whole_steamed_chicken_ordered = int(request.form.get('WSC_quantity'))
        total_cost = f"{float(request.form.get('initial_cost')):.2f}"
        item_amts_ordered = [steamed_chicken_rice_ordered, half_steamed_chicken_ordered, whole_steamed_chicken_ordered]
        items = ['Steamed Chicken Rice', 'Half Steamed Chicken', 'Whole Steamed Chicken']
        items_ordered = []
        print(item_amts_ordered)
        for x in range(len(item_amts_ordered)):
            if item_amts_ordered[x] > 0:
                items_ordered.append(items[x])
        price_list = []
        print(items_ordered)
        for item in items_ordered:
            item_base_price = item_prices[item]
            index = items.index(item)
            item_price = item_base_price * item_amts_ordered[index]
            price_list.append(item_price)
        item_amts_ordered_filtered = [x for x in item_amts_ordered if x > 0]
        print(item_amts_ordered_filtered)
        total_amts = sum(item_amts_ordered_filtered)
        print(total_amts)
        return render_template('customer/checkout.html', items_ordered = items_ordered, price_list = price_list, total_cost = total_cost, item_amts_ordered_filtered = item_amts_ordered_filtered)
    else:
        print('its get')
        return render_template('customer/js_customer_home.html')


# here is where they scan the qr code and submit ss of paynow
@app.route('/payment', methods=['POST'])
def payment():
    itemidk = 'items'
    # use this ast thingie to convert '[3, 1]' into an actual list [3, 1]
    item_amts_ordered_filtered = ast.literal_eval(request.form.get('item_amts_ordered_filtered'))
    print(item_amts_ordered_filtered)
    total_amts = 0
    for item_amt in item_amts_ordered_filtered:
        total_amts += int(item_amt)
    print(total_amts)
    if total_amts == 1:
        itemidk = 'item'
    total_cost = request.form.get('total_cost')
    items_ordered = ast.literal_eval(request.form.get('items_ordered'))
    price_list = ast.literal_eval(request.form.get('price_list'))
    order_datetime = datetime.now() + timedelta(hours=8)
    order_datetime = order_datetime.strftime("%Y-%m-%d %H:%M:%S")
    order_date = order_datetime.split(' ')[0]
    order_time = order_datetime.split(' ')[1]
    # 'APPEND ORDER DETAILS TO DATABASE CODE' HERE
    return render_template('customer/payment.html', items_ordered = items_ordered, price_list = price_list, item_amts_ordered_filtered = item_amts_ordered_filtered, total_cost = total_cost, total_amts = total_amts, itemsss = itemidk, order_date = order_date, order_time = order_time)

# this will use socket.io to handle the form and send data to the admin dashboard


# this is where the YOLO will take out all the impt info and verify, as well as upload the data to a database
@app.route('/confirmation', methods=['POST'])
def confirmation():
    items_ordered = ast.literal_eval(request.form.get('items_ordered'))
    price_list = ast.literal_eval(request.form.get('price_list'))
    item_amts_ordered_filtered = ast.literal_eval(request.form.get('item_amts_ordered_filtered'))
    total_cost = request.form.get('total_cost')
    order_date = request.form.get('order_date')
    order_time = request.form.get('order_time')
    return render_template('customer/confirmation.html', items_ordered = items_ordered, price_list = price_list, item_amts_ordered_filtered = item_amts_ordered_filtered, total_cost = total_cost, order_date = order_date, order_time = order_time)

# do stall owner stuff only after u finish all the customer stuff
@app.route('/admin_home', methods=['POST'])
def admin_home():
    return render_template('customer/admin_home.html')


if __name__ == '__main__':
    socketio.run(app)