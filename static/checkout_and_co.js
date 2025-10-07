// for pressing home button and remembering the order

const home_button = document.querySelector('#home_button')
const remember_order = document.querySelector('#remember_order')

home_button.addEventListener('click', function() {
    remember_order.submit();
})

// shi from payment.html
const order_time_hour = document.querySelector('#order_time_hour').textContent
const order_time_min = document.querySelector('#order_time_minute').textContent
const hour = document.querySelector('#collection_hour')
const minute = document.querySelector('#collection_minute')

// for hour

const decrease_hour = document.querySelector('#decrease_hour')
const increase_hour = document.querySelector('#increase_hour')

increase_hour.addEventListener('click', function() {
    let initial_hour = parseInt(hour.textContent);
    if (initial_hour < 17) {
        let next_hour = initial_hour + 1;
        let new_hour = next_hour.toString();
        hour.textContent = new_hour
    }

    else {
        hour.textContent = order_time_hour
        minute.textContent = order_time_min
    }
})

decrease_hour.addEventListener('click', function() {
    let initial_hour = parseInt(hour.textContent)
    let min_hour = parseInt(order_time_hour)
    if (initial_hour > min_hour) {
        let next_hour = initial_hour - 1;
        let new_hour = next_hour.toString();
        hour.textContent = new_hour
        if (next_hour == min_hour) {
            minute.textContent = order_time_min
        }
    }

    // the else below should be next_min == 0
    else {
        hour.textContent = '17'
    }
})


// for minute
const decrease_min = document.querySelector('#decrease_min')
const increase_min = document.querySelector('#increase_min')

increase_min.addEventListener('click', function() {
    let initial_min = parseInt(minute.textContent);
    let min_min = '00'
    if (hour.textContent == order_time_hour) {
        min_min = order_time_min
    }
    if (initial_min < 55) {
        let next_min = initial_min + 5;
        let new_min = next_min.toString();

        if (next_min == 5) {
            new_min = '0' + new_min
        }

        minute.textContent = new_min
    }

    else {
        minute.textContent = min_min
    }
})

decrease_min.addEventListener('click', function() {
    let initial_min = parseInt(minute.textContent)
    let min_min = '00'
    if (hour.textContent == order_time_hour) {
        min_min = order_time_min
    }
    if (initial_min > parseInt(min_min)) {
        let next_min = initial_min - 5;
        let new_min = next_min.toString();

        if (next_min <= 5) {
            new_min = '0' + new_min
        }

        minute.textContent = new_min
    }

    // the else below should be next_min == 0
    else {
        minute.textContent = '55'
    }
})

const ampm = document.querySelector('#collection_ampm')

const payment_hiddenform = document.querySelector('#hidden_form')

const hour_input = document.querySelector('#collection_hour_input')
const minute_input = document.querySelector('#collection_minute_input')
const ampm_input = document.querySelector('#collection_ampm_input')

payment_hiddenform.addEventListener('submit', function() {
    hour_input.value = hour.textContent;
    minute_input.value = minute.textContent;
    ampm_input.value = ampm.value;
})