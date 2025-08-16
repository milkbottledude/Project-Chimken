const socket = io('/admin');
const orderdiv = document.querySelector('#orders');
const data_holder = document.querySelector('#data-holder')
const msgList = JSON.parse(data_holder.dataset.msgList);


function to_dashboard(single_msg) {
  var newdiv = document.createElement('div');
  newdiv.classList.add('dashboard_order');
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
  d_button.classList.add('dismiss_button');
  d_button.textContent = 'X';
  newdiv.appendChild(d_button)
  orderdiv.prepend(newdiv);
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

const dismissed_container = document.querySelector('#not_impt_orders');
const dismissal_buttons = document.querySelectorAll('.dismiss_button');

dismissal_buttons.forEach(
  button => {
    button.addEventListener('click', function() {
      let button_id = button.id;
      order_id = button_id.slice(0, -7);
      let order_box = document.querySelector(`#${order_id}`);
      order_box.classList.add('dismissed_order');
      dismissed_container.prepend(order_box);
    })
  }
)