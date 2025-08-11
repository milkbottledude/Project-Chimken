const socket = io('/admin');
const orderdiv = document.querySelector('#orders')

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
    var newdiv = document.createElement('div');
    newdiv.classList.add('dashboard_order');
    msg_array = msg.split('_')
    for (i = 0; i <= 3; i++) {
      var newp = document.createElement('p');
      msg_part = msg_array[i];
      if (i == 1) {
        split_part = msg_part.split(': ');
        newp.textContent = split_part[0] + ': ';
        pt_two = split_part[1].split(', ')
        for (x = 0; x <= pt_two.length; x++) {
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
    orderdiv.appendChild(newdiv);
    console.log('child appended');
  });

  // detect disconnects
socket.on('disconnect', () => {
    console.log('Disconnected from /admin');
  });