// for pressing home button and remembering the order

const home_button = document.querySelector('#home_button')
const remember_order = document.querySelector('#remember_order')

home_button.addEventListener('click', function() {
    remember_order.submit();
})

// shi from payment.html

const decrease_min = document.querySelector('#decrease_min')
const increase_min = document.querySelector('#increase_min')
const minute = document.querySelector('#collection_minute')

increase_min.addEventListener('click', function() {
    let initial_min = parseInt(minute.textContent);
    if (initial_min < 55) {
        let next_min = initial_min + 5;
        let new_min = next_min.toString();

        if (next_min == 5) {
            new_min = '0' + new_min
        }

        minute.textContent = new_min
    }

    else {
        minute.textContent = '00'
    }
})

decrease_min.addEventListener('click', function() {
    let initial_min = parseInt(minute.textContent)
    if (initial_min > 0) {
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

const hour = document.querySelector('#collection_hour')
const ampm = document.querySelector('#collection_ampm')

const payment_hiddenform = document.querySelector('#hidden_form')

const hour_input = document.querySelector('#collection_hour_input')
const minute_input = document.querySelector('#collection_minute_input')
const ampm_input = document.querySelector('#collection_ampm_input')

payment_hiddenform.addEventListener('submit', function() {
    hour_input.value = hour.value;
    minute_input.value = minute.textContent;
    ampm_input.value = ampm.value;
})