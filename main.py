import pandas as pd
import numpy as np
from flask import Flask, render_template, request, session, redirect
from flask_socketio import SocketIO, send
import ast
from datetime import datetime, timedelta, date
from google.cloud import firestore
from zoneinfo import ZoneInfo


app = Flask(__name__)
app.config['SECRET_KEY'] = 'not_the_actual_key'
socketio = SocketIO(
    app,
    async_mode='threading',
    cors_allowed_origins=["https://5000-cs-700308306001-default.cs-asia-southeast1-fork.cloudshell.dev", "https://xenon-height-425100-i6.et.r.appspot.com"]
)
# print(f"SocketIO async mode: {socketio.async_mode}")
# print('NIGAAAAAAAAAAA')

stall_phone_number = None

item_prices = {
    'Steamed Chicken Rice': 5.00,
    'Half Steamed Chicken': 15.00,
    'Whole Steamed Chicken': 20.00,
    'Rice Packet': 1.00
}

items = ['Steamed Chicken Rice', 'Half Steamed Chicken', 'Whole Steamed Chicken', 'Rice Packet']


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
SSL_name = 'S S Lee'
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
        print('ADMINNNNNNN DETECTEDDDDDDDDDDDDDDDD')
        mass_queryplan = (orders_db.collection('SSL_orders')
                    .where('date_str', '==', date.today().strftime("%Y-%m-%d"))
                    .order_by('time_str', direction=firestore.Query.ASCENDING))

        mass_docs = mass_queryplan.get() # TRY .STREAM AS WELL, SEE IF IT WORKS, COS STREAM SUPPOSED TO BE MORE EFFICIENT, LOADS 1 AT A TIME
        print(mass_docs)
        lesgo_dbs_list = []
        for doc in mass_docs:
            doc_dict = doc.to_dict()

            ISSIT_REALLY_A_DICT = {
                'Order Number': 666,
                'Items Ordered': 777,
                'Total Cost': 888,
                'Collection Time': 999            
            }

            ISSIT_REALLY_A_DICT['Order Number'] = doc_dict['order_no']
            ISSIT_REALLY_A_DICT['Items Ordered'] = doc_dict['item_amts_ordered']
            ISSIT_REALLY_A_DICT['Total Cost'] = doc_dict['total_cost']
            ISSIT_REALLY_A_DICT['Collection Time'] = doc_dict['collection_time']
            print('assigned values to issitdict yuhhhhhhhhhhh')
            print(ISSIT_REALLY_A_DICT)

            # ASSIGN DOC_DICT VALUES TO ISSITRLLYDICT continueeeeeeeeeeeeheree

            lesgo_db = ''
            for key, value in ISSIT_REALLY_A_DICT.items():
                if key == 'Items Ordered':
                    print(value)
                    value = ', '.join(value)
                key = key.replace('_', ' ')
                lesgo_db = lesgo_db + key + ': ' + str(value) + '_'
            print(lesgo_db)
            lesgo_dbs_list.append(lesgo_db[:-1])
        print(len(lesgo_dbs_list))
        print('SKSKSKSLSKLSLLSLKSLSLLSLKSLKSLK HOW LONG THE LIST BRuh')
        return render_template('dashboard.html', name = SSL_name, lesgo_dbs_list = lesgo_dbs_list)
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
    'item_amts_ordered': [],
    'total_cost': None,
    'order_datetime_obj': None,
    'date_str': None,
    'time_str': None,
    'order_no': None,
    'payment': None
}

dashboard_data = {
    'Order Number': 111,
    'Items Ordered': 222,
    'Total Cost': 444,
    'Collection Time': 555,
    'order_ID': None,
}


# here is where the ngas can see what they ordered
@app.route('/checkout', methods=['GET', 'POST']) # Maybe add a msg as well to say 'u hvnt ordered shi', but not yet focus on basics first
def checkout():

# threading over eventlet works, yay
    # try:
    #     print("Starting Firestore query...")
    #     queryplan = orders_db.collection('SSL_orders').order_by('order_datetime_obj', direction=firestore.Query.DESCENDING).limit(1)
    #     print('balls')
    #     queryresults = queryplan.get(timeout=10)  # 10 second timeout
    #     print(f"Query completed. Found {len(queryresults)} results")
    #     latest_order = queryresults[0] if queryresults else None
    #     print("Query successful")
    # except Exception as e:
    #     print(f"Query error: {e}")
    #     latest_order = None


    if request.method == 'POST':
        SCR_amt = int(request.form.get('SCR_quantity'))
        HSC_amt = int(request.form.get('HSC_quantity'))
        WSC_amt = int(request.form.get('WSC_quantity'))
        RP_amt = int(request.form.get('RP_quantity'))
        total_cost = f"{float(request.form.get('initial_cost')):.2f}"
        db_data['total_cost'] = total_cost
        item_amts_ordered = [SCR_amt, HSC_amt, WSC_amt, RP_amt]
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
        # adding to dashboard dict
        dashboard_data['Items Ordered'] = items_ordered.copy()
        dashboard_data['Total Cost'] = total_cost
        print(items_ordered)
        len(item_amts_ordered_filtered)
        print('FUCKKKKKKKKKKKKKKKKKK')
        for i in range(len(item_amts_ordered_filtered)):
            print('FUCKKKKKKKKKKKKKKKKKK')
            print(len(item_amts_ordered_filtered))
            item = items_ordered[i]
            item_amt = str(item_amts_ordered_filtered[i])
            dashboard_data['Items Ordered'][i] = item + ' - ' + item_amt
            db_data['item_amts_ordered'].append(item + ' - ' + item_amt)
        print(item_amts_ordered)
        print('BETTER NOT BE 22222222222222222222')
        print(dashboard_data['Items Ordered'])
        print('BETTER NOT BE 22222222222222222222')
        total_amts = sum(item_amts_ordered_filtered)
        return render_template('customer/checkout.html', items_ordered = items_ordered, price_list = price_list, total_cost = total_cost, item_amts_ordered_filtered = item_amts_ordered_filtered, item_amts_ordered = item_amts_ordered)
    else:
        print('its get')
        return redirect('/')



# here is where they scan the qr code and submit ss of paynow
@app.route('/payment', methods=['GET', 'POST'])
def payment():

    print('BETTER NOT BE 22222222222222222222')
    print(dashboard_data['Items Ordered'])
    print('BETTER NOT BE 22222222222222222222')


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
        db_data['date_str'] = order_date
        db_data['time_str'] = order_time

        return render_template('customer/payment.html', items_ordered = items_ordered, price_list = price_list, item_amts_ordered_filtered = item_amts_ordered_filtered, total_cost = total_cost, total_amts = total_amts, itemsss = itemidk, order_date = order_date, order_time = order_time, item_amts_ordered = item_amts_ordered)

# this will use socket.io to handle the form and send data to the admin dashboard


# this is where the YOLO will take out all the impt info and verify, as well as upload the data to a database
@app.route('/confirmation', methods=['GET', 'POST'])
def confirmation():
    if request.method == 'GET':
        return redirect('/')
    else:

        print('BETTER NOT BE 22222222222222222222')
        print(dashboard_data['Items Ordered'])
        print('BETTER NOT BE 22222222222222222222')


        
        collection_hour = request.form.get('collection_hour_input')
        collection_minute = request.form.get('collection_minute_input')
        collection_ampm = request.form.get('collection_ampm_input')
        dashboard_data['Collection Time'] = f'{collection_hour}:{collection_minute} {collection_ampm}'
        db_data['collection_time'] = f'{collection_hour}:{collection_minute} {collection_ampm}'
        print('CHECK COLLECTION TIME HEREEEEEEEEEEEEEEEEEEE')
        print(collection_hour, collection_minute, collection_ampm)
        items_ordered = ast.literal_eval(request.form.get('items_ordered'))
        price_list = ast.literal_eval(request.form.get('price_list'))
        item_amts_ordered_filtered = ast.literal_eval(request.form.get('item_amts_ordered_filtered'))
        total_cost = db_data['total_cost']
        order_no = request.form.get('order_no')
        order_date = request.form.get('order_date')
        order_time = request.form.get('order_time')


        # GETTING ORDER NUMBER FROM DB      .
        #                               HERE
        print('getting order number from db AGHHHHHHHHHHHH')
        order_no = 1
        order_id_no = 1
        order_datetime_obj = datetime.now(ZoneInfo("Asia/Kuala_Lumpur"))
        queryplan = orders_db.collection('SSL_orders').order_by('order_datetime_obj', direction=firestore.Query.DESCENDING).limit(1)
        queryresults = queryplan.get()
        latest_order = queryresults[0]
        if latest_order:
            latest_order = latest_order.to_dict()
            print('LATESTTTTTTTTTTTTTT ORDER FROM DB')
            print(latest_order)
            order_id_no = str(int(latest_order['order_ID'][-1]) + 1)
            print('NIGGGGGGGGGGGGGGGGGGGGGG')
            print(order_id_no)
            print(latest_order['order_ID'][1])
            print('NIGGGGGGGGGGGGGGGGGGGGGG')

            order_date = latest_order['order_datetime_obj'].date()
            current_date = order_datetime_obj.date()
            if order_date == current_date:
                order_no = int(latest_order['order_no']) + 1
        dashboard_data['Order Number'] = order_no
        db_data['order_no'] = order_no
        db_data['order_ID'] = str(current_date) + '_' + str(order_id_no)
        dashboard_data['order_ID'] = 'id' + str(current_date) + 'n' + str(order_id_no)
        db_data['order_datetime_obj'] = order_datetime_obj
        db_data['payment'] = 'PENDING'

        # SENDING ORDER DEETS TO DB
        print('Sending order details to firestore db')
        print(db_data)
        orders_db.collection('SSL_orders').document(db_data['order_ID']).set(db_data)
        print('Order details sent to firestore db')


        # dashboard code below, to be moved further down to confirmation.html when deploying app (DONE)
        go_db = ''
        print(dashboard_data)
        for key, value in dashboard_data.items():
            key = key + ': '
            print(key, value)
            if key == 'Items Ordered: ':
                print(value)
                value = ', '.join(value)
            elif key == 'order_ID: ':
                key = ''
            go_db = go_db + key + str(value) + '_'
        print(go_db)
        print('SOCKETINGGGGGGGGGGGGGGGGGGG')
        socketio.send(go_db[:-1], namespace='/admin')
        print('SOCKETeeeeeeeeeeeeeD')        


        return render_template('customer/confirmation.html', items_ordered = items_ordered, price_list = price_list, item_amts_ordered_filtered = item_amts_ordered_filtered, total_cost = total_cost, order_no = order_no, order_date = order_date, order_time = order_time, collection_hour = collection_hour, collection_minute = collection_minute, collection_ampm = collection_ampm)


if __name__ == '__main__':
    socketio.run(app, host="0.0.0.0", port=5000, debug=True)
