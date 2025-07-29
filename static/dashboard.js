const socket = io('/admin')

socket.on('new_order', (dashboard_data) => {
    const ordersDiv = document.querySelector('#orders');
    const p = document.createElement('p');
    p.innerText = "New order: " + JSON.stringify(data);
    ordersDiv.appendChild(p);
  });