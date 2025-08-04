import pandas as pd
import numpy as np
from flask import Flask, render_template, request, session, redirect
from flask_socketio import SocketIO, send
import ast
from datetime import datetime, timedelta
from google.cloud import firestore
from zoneinfo import ZoneInfo


app = Flask(__name__)
app.config['SECRET_KEY'] = 'not_the_actual_key'
socketio = SocketIO(
    app, cors_allowed_origins=["https://5000-cs-700308306001-default.cs-asia-southeast1-fork.cloudshell.dev"
])


stall_phone_number = None

item_prices = {
    'Steamed Chicken Rice': 5.00,
    'Half Steamed Chicken': 15.00,
    'Whole Steamed Chicken': 20.00,
    'Rice Packet': 1.00
}

@app.route('/', methods=['GET', 'POST'])
def login():
    print('ajimaru-ajimaru')
    invalid_id = False
    if invalid_id:
        print('wrong IDDDDDDDDDDDDD')
        return render_template('login.html')
    else:
        return render_template('login.html')

# Hawker Admin home below
SSL_password = 'SSL01'
SSL_name = 'Sing Soon Lee'
# do stall owner stuff only after u finish all the customer stuff
@app.route('/admin_home', methods=['GET', 'POST'])
def admin_home():
    if request.method == 'POST':
        hawker_id = request.form.get('hawker_id_input')
        if hawker_id == SSL_password:
            session['is_admin'] = True
            return redirect('/admin_home')
        else:
            return render_template('login.html', invalid_id = True)
    if session.get('is_admin'):
        return render_template('dashboard.html', name = SSL_name)
    else:
        return redirect('/')

# hawker dashboard side, for receiving socket signals
@socketio.on('order', namespace='/admin')
def handle_order(order_data):
    print('Received order:', order_data)




# add python code for customer home below
SCR_amt = 0
HSC_amt = 0
WSC_amt = 0
RP_amt = 0
initial_cost = 0


@app.route('/js_home', methods=['GET', 'POST'])
def js_home():
    global SCR_amt, HSC_amt, WSC_amt, RP_amt, initial_cost
    if request.method == 'POST':
        print('its posttttttttttttttttttttttttttttttt')
        print(request.form.get('item_amts_ordered'))
        amts = ast.literal_eval(request.form.get('item_amts_ordered'))
        initial_cost = request.form.get('total_cost')[:-3]
        SCR_amt = amts[0]
        HSC_amt = amts[1]
        WSC_amt = amts[2]
        RP_amt = amts[3]
        print(SCR_amt, HSC_amt, WSC_amt, RP_amt)
    else:
        print('its get')
        SCR_amt = 0
        HSC_amt = 0
        WSC_amt = 0
        RP_amt = 0
        initial_cost = 0
    return render_template('customer/js_customer_home.html', SCR_quantity = SCR_amt, HSC_quantity = HSC_amt, WSC_quantity = WSC_amt, RP_quantity = RP_amt, initial_cost = initial_cost)


# firestore database shi here
orders_db = firestore.Client()

db_data = {
    'order_ID': None,
    'item_amts_ordered': None,
    'total_cost': None,
    'order_datetime_obj': None,
    'order_no': None,
    # 'payment': 'NOT PAID'
}

dashboard_data = {
    'order_no': 111,
    'items_ordered': 222,
    'item_amts_filtered': 333,
    'total_cost': 444,
}


# here is where the ngas can see what they ordered
@app.route('/checkout', methods=['GET', 'POST']) # Maybe add a msg as well to say 'u hvnt ordered shi', but not yet focus on basics first
def checkout():
    if request.method == 'POST':
        SCR_amt = int(request.form.get('SCR_quantity'))
        HSC_amt = int(request.form.get('HSC_quantity'))
        WSC_amt = int(request.form.get('WSC_quantity'))
        RP_amt = int(request.form.get('RP_quantity'))
        total_cost = f"{float(request.form.get('initial_cost')):.2f}"
        item_amts_ordered = [SCR_amt, HSC_amt, WSC_amt, RP_amt]
        items = ['Steamed Chicken Rice', 'Half Steamed Chicken', 'Whole Steamed Chicken', 'Rice Packet']
        items_ordered = []
        print(item_amts_ordered)
        db_data['item_amts_ordered'] = item_amts_ordered # appending unfiltered item amts list to db dict here, n not at payment()
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
        # adding to dashboard dict
        dashboard_data['item_amts_filtered'] = item_amts_ordered_filtered
        dashboard_data['items_ordered'] = items_ordered
        dashboard_data['total_cost'] = total_cost

        # to be moved further down when deploying app

        go_db = ''
        for key, value in dashboard_data.items():
            go_db = go_db + key + ': ' + str(value) + ', '         
        print('SOCKETINGGGGGGGGGGGGGGGGGGG')
        socketio.send(go_db, namespace='/admin')
        print('SOCKETeeeeeeeeeeeeeD')



        total_amts = sum(item_amts_ordered_filtered)
        print(total_amts)
        return render_template('customer/checkout.html', items_ordered = items_ordered, price_list = price_list, total_cost = total_cost, item_amts_ordered_filtered = item_amts_ordered_filtered, item_amts_ordered = item_amts_ordered)
    else:
        print('its get')
        return redirect('/')



# here is where they scan the qr code and submit ss of paynow
@app.route('/payment', methods=['GET', 'POST'])
def payment():
    if request.method == 'GET':
        return redirect('/')
    else:
        itemidk = 'items'
        item_amts_ordered = ast.literal_eval(request.form.get('item_amts_ordered'))
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
        order_datetime_obj = datetime.now(ZoneInfo("Asia/Kuala_Lumpur"))
        order_datetime = order_datetime_obj.strftime("%Y-%m-%d %H:%M:%S")
        order_date = order_datetime.split(' ')[0]
        order_time = order_datetime.split(' ')[1]
        # 'APPEND ORDER DETAILS TO DATABASE CODE' HERE
        order_no = 1
        order_id_no = 1
        # db_data['order_ID'] = '_'.join(['001', order_date]) # ONLY USE THIS IF DOCUMENT HAS NO ROWS YET
        queryplan = orders_db.collection('SSL_orders').order_by('created_at', direction=firestore.Query.DESCENDING).limit(1)
        queryresults = queryplan.stream()
        latest_order = next(queryresults, None)
        if latest_order:
            latest_order = latest_order.to_dict()
            order_id_no = latest_order['order_ID'] + 1
            order_date = latest_order['order_datetime_obj'].date()
            if order_date == datetime.now(ZoneInfo("Asia/Kuala_Lumpur")).date():
                order_no = int(latest_order['order_no']) + 1
        dashboard_data['order_no'] = order_no
        # socketing to dashboard.js to display in dashboard.html
        # print('SOCKETINGGGGGGGGGGGGGGGGGGG')
        # socketio.send(dashboard_data, namespace='/admin')
        # print('SOCKETeeeeeeeeeeeeeD')
        db_data['order_ID'] = str(order_id_no) + '_' + str(order_date)
        db_data['total_cost'] = float(total_cost)
        db_data['order_datetime_obj'] = order_datetime_obj

        return render_template('customer/payment.html', items_ordered = items_ordered, price_list = price_list, item_amts_ordered_filtered = item_amts_ordered_filtered, order_no = order_no, total_cost = total_cost,total_amts = total_amts, itemsss = itemidk, order_date = order_date, order_time = order_time, item_amts_ordered = item_amts_ordered)

# this will use socket.io to handle the form and send data to the admin dashboard


# this is where the YOLO will take out all the impt info and verify, as well as upload the data to a database
@app.route('/confirmation', methods=['GET', 'POST'])
def confirmation():
    if request.method == 'GET':
        return redirect('/')
    else:
        collection_hour = request.form.get('collection_hour_input')
        collection_minute = request.form.get('collection_minute_input')
        collection_ampm = request.form.get('collection_ampm_input')
        print('CHECK COLLECTION TIME HEREEEEEEEEEEEEEEEEEEE')
        print(collection_hour, collection_minute, collection_ampm)
        items_ordered = ast.literal_eval(request.form.get('items_ordered'))
        price_list = ast.literal_eval(request.form.get('price_list'))
        item_amts_ordered_filtered = ast.literal_eval(request.form.get('item_amts_ordered_filtered'))
        total_cost = db_data['total_cost']
        order_no = request.form.get('order_no')
        order_date = request.form.get('order_date')
        order_time = request.form.get('order_time')
        # SENDING ORDER DEETS TO DB
        print('Sending order details to firestore db')
        print(db_data)
        # SEND REQUEST TO STALL-OWNER HOME TO FETCH ORDER DETAILS FROM DB      . ONLY OTHER TIME IT WILL FETCH FROM DB IS WHEN THEY LOG IN.
        #                                                                 HERE
        # socketio.emit('new_order', dashboard_data, namespace='/admin')
        orders_db.collection('SSL_orders').document(db_data['order_ID']).set(db_data)
        return render_template('customer/confirmation.html', items_ordered = items_ordered, price_list = price_list, item_amts_ordered_filtered = item_amts_ordered_filtered, total_cost = total_cost, order_no = order_no, order_date = order_date, order_time = order_time, collection_hour = collection_hour, collection_minute = collection_minute, collection_ampm = collection_ampm)


if __name__ == '__main__':
    socketio.run(app, debug=True)
