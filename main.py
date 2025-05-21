import pandas as pd
import numpy as np
from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def login():
    return render_template('login.html')

# add python code for home below
@app.route('/home')
def home():
    return render_template('customer_home.html')

# here is where the ngas can see what they ordered
@app.route('/checkout', methods=['POST'])
def checkout():
    return render_template('checkout.html')

# here is where they scan the qr code and submit ss of paynow
@app.route('/payment', methods=['POST'])
def payment():
    return render_template('payment.html')

# do stall owner stuff only after u finish all the customer stuff
@app.route('/admin_home', methods=['POST'])
def admin_home():
    return render_template('admin_home.html')





if __name__ == "__main__":
    app.run(debug=True)