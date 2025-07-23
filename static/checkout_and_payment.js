// for pressing home button and remembering the order

const home_button = document.querySelector('#home_button')
const remember_order = document.querySelector('#remember_order')

home_button.addEventListener('click', function() {
    remember_order.submit();
})

// shi from payment.html

const hour = document.querySelector('#hour')
const minute = document.querySelector('#minute')

