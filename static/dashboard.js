const socket = io('/admin');
const orderdiv = document.querySelector('#orders')

socket.on('connect', () => {
    console.log('Connected to /admin');
    socket.send('Hello from client!');
  });

socket.on('message', (msg) => {
    console.log('Message from server:', msg);
    socket.send(msg);
    var newp = document.createElement('p');
    socket.send('p created')
    newp.textContent = msg;
    orderdiv.appendChild(newp);
    socket.send('p added to div')
    console.log('child appended');
  });

  // detect disconnects
socket.on('disconnect', () => {
    console.log('Disconnected from /admin');
  });