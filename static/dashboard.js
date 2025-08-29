const socket = io('/admin', {transport: ['websocket', 'polling']});
const orderdiv = document.querySelector('#orders');
const not_impt_ordersdiv = document.querySelector('#not_impt_orders')
const data_holder = document.querySelector('#data-holder')
const msgList = JSON.parse(data_holder.dataset.msgList);


function to_dashboard(single_msg) {
  var newdiv = document.createElement('div');
  msg_array = single_msg.split('_')
  newdiv.id = msg_array[4]
  for (i = 0; i <= 3; i++) {
    var newp = document.createElement('p');
    msg_part = msg_array[i];
    if (i == 1) {
      split_part = msg_part.split(': ');
      newp.textContent = split_part[0] + ': ';
      pt_two = split_part[1].split(', ')
      for (x = 0; x < pt_two.length; x++) {
        var lilspan = document.createElement('span');
        lilspan.textContent = pt_two[x];
        lilspan.classList.add('blocked');
        newp.appendChild(lilspan);
      }
    } else {
      newp.textContent = msg_part;
    }
    newp.classList.add('order_p')
    newdiv.appendChild(newp);
  }
// now adding dismiss_button
  var d_button = document.createElement('button');
  d_button.id = msg_array[4] + '_button';
  d_button.textContent = 'V';
  newdiv.appendChild(d_button)
  console.log(msg_array[5])
  if (msg_array[5] == 'payment: DISMISSED') {
    console.log('dismissed hereE');
    newdiv.classList.add('dismissed_order');
    d_button.classList.add('retain_button');
    not_impt_ordersdiv.prepend(newdiv);
  } else {
    console.log('not dismissed hereE');
    newdiv.classList.add('dashboard_order');
    d_button.classList.add('dismiss_button');
    orderdiv.prepend(newdiv);
  }    
  console.log('child appended');
}

for (m = 0; m < msgList.length; m++) {
  to_dashboard(msgList[m]);
}


// flask-socketio shi below

socket.on('connect', () => {
    console.log('Connected to /admin');
    socket.send('Hello from client!');
  });

// socket.on('message', (msg) => {
//     console.log('Message from server:', msg);
//     socket.send(msg);
//     var newp = document.createElement('p');
//     newp.classList.add('dashboard_order')
//     socket.send('p created')
//     newp.textContent = msg;
//     orderdiv.appendChild(newp);
//     socket.send('p added to div')
//     console.log('child appended');
//   });


socket.on('message', (msg) => {
    console.log('Message from server:', msg);
    socket.send(msg);
    to_dashboard(msg);
  });

  // detect disconnects
socket.on('disconnect', () => {
    console.log('Disconnected from /admin');
  });


  
// js for dismissal button

const orders_container = document.querySelector('#all_orders');
const dismissed_container = document.querySelector('#not_impt_orders');
const retained_container = document.querySelector('#orders');

    // stuff for editing fields in firestore docs
const firebaseConfig = {
  apiKey: "AIzaSyB4TCkrAy6Gt_CF0TdDkOvlZE_AUUZ26cw",
  projectId: "xenon-height-425100-i6"
}

firebase.initializeApp(firebaseConfig);
const db = firebase.firestore();

async function updateField(docRef, fieldName, newValue) {
  await docRef.update({
    [fieldName]: newValue
  });
  console.log(`${fieldName} is now ${newValue}`);
}

orders_container.addEventListener('click', async function(event) {
  const button = event.target;
  const button_id = button.id;
  order_id = button_id.slice(0, -7);
  const docRef = db.collection('SSL_orders').doc(order_id);
  if (button.classList.contains('dismiss_button')) {
    // order_id = button_id.slice(0, -7);
    console.log(order_id);
    // changing firestore doc field's value 
    await updateField(docRef, 'payment', 'DISMISSED');
    let order_box = document.querySelector(`#${order_id}`);
    order_box.classList.add('dismissed_order');
    button.classList.add('retain_button');
    order_box.classList.remove('dashboard_order');
    button.classList.remove('dismiss_button');
    dismissed_container.prepend(order_box);  
  } else if (button.classList.contains('retain_button')) {
    // let button_id = button.id;
    // order_id = button_id.slice(0, -7);
    // changing firestore doc field's value 
    await updateField(docRef, 'payment', 'PENDING');
    let order_box = document.querySelector(`#${order_id}`);
    order_box.classList.add('dashboard_order');
    button.classList.add('dismiss_button');
    order_box.classList.remove('dismissed_order');
    button.classList.remove('retain_button');
    retained_container.prepend(order_box);
  }
});