import pandas as pd
import numpy as np
from flask import Flask, render_template, request
from flask_socketio import SocketIO

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
@app.route('/home')
def home():
    return render_template('customer/customer_home.html')


# here is where the ngas can see what they ordered
@app.route('/checkout', methods=['GET', 'POST']) # Maybe add a msg as well to say 'u hvnt ordered shi', but not yet focus on basics first
def checkout():
    if request.method == 'POST':
        steamed_chicken_rice_ordered = int(request.form.get('steamed_chicken_rice_amt'))
        half_steamed_chicken_ordered = int(request.form.get('half_steamed_chicken_amt'))
        whole_steamed_chicken_ordered = int(request.form.get('whole_steamed_chicken_amt'))
        item_amts_ordered = [steamed_chicken_rice_ordered, whole_steamed_chicken_ordered, half_steamed_chicken_ordered]
        items = ['Steamed Chicken Rice', 'Whole Steamed Chicken', 'Half Steamed Chicken']
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
        total_cost = sum(price_list)
        item_amts_ordered_filtered = [x for x in item_amts_ordered if x > 0]
        return render_template('customer/checkout.html', items_ordered = items_ordered, price_list = price_list, total_cost = total_cost, item_amts_ordered_filtered = item_amts_ordered_filtered)
    else:
        return render_template('customer/customer_home.html')


# here is where they scan the qr code and submit ss of paynow
@app.route('/payment', methods=['POST'])
def payment():
    total_cost = request.form.get('total_cost')
    print(total_cost)
    return render_template('customer/payment.html', total_cost = total_cost)

# this will use socket.io to handle the form and send data to the admin dashboard


# this is where the YOLO will take out all the impt info and verify, as well as upload the data to a database
@app.route('/confirmation', methods=['POST'])
def confirmation():
    return render_template('customer/confirmation.html')

# do stall owner stuff only after u finish all the customer stuff
@app.route('/admin_home', methods=['POST'])
def admin_home():
    return render_template('customer/admin_home.html')


if __name__ == '__main__':
    socketio.run(app)