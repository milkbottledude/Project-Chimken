// default constants
const steamed_chicken_rice_price = 5;
const half_steamed_chicken_price = 15;
const whole_steamed_chicken_price = 20;

// total cost b4 gst and allat
const initial_cost = document.getElementById('initial_cost')
const checkout_button = document.getElementById('checkout_icon')

// for steamed chicken rice
const down_SCR = document.getElementById('decrease_SCR')
const up_SCR = document.getElementById('increase_SCR')
const SCR_quantity = document.getElementById('SCR_quantity')

down_SCR.addEventListener('click', function() {
    let current_SCR_quantity = parseInt(SCR_quantity.textContent)

    if (current_SCR_quantity > 0) {
        current_SCR_quantity -= 1
        SCR_quantity.textContent = current_SCR_quantity

        let current_cost = parseInt(initial_cost.textContent)
        current_cost -= steamed_chicken_rice_price
        initial_cost.textContent = current_cost

        if (current_cost == 0) {
            checkout_button.style.display ='none'
        }
    }

})

up_SCR.addEventListener('click', function() {
    let current_SCR_quantity = parseInt(SCR_quantity.textContent)
    current_SCR_quantity += 1
    SCR_quantity.textContent = current_SCR_quantity

    let current_cost = parseInt(initial_cost.textContent)
    current_cost += steamed_chicken_rice_price
    initial_cost.textContent = current_cost
    checkout_button.style.display = 'block'
})


// for half steamed chicken
const down_HSC = document.getElementById('decrease_HSC')
const up_HSC = document.getElementById('increase_HSC')
const HSC_quantity = document.getElementById('HSC_quantity')

down_HSC.addEventListener('click', function() {
    let current_HSC_quantity = parseInt(HSC_quantity.textContent)

    if (current_HSC_quantity > 0) {
        current_HSC_quantity -= 1
        HSC_quantity.textContent = current_HSC_quantity

        let current_cost = parseInt(initial_cost.textContent)
        current_cost -= half_steamed_chicken_price
        initial_cost.textContent = current_cost

        if (current_cost == 0) {
            checkout_button.style.display ='none'
        }
    }
})

up_HSC.addEventListener('click', function() {
    let current_HSC_quantity = parseInt(HSC_quantity.textContent)
    current_HSC_quantity += 1
    HSC_quantity.textContent = current_HSC_quantity

    let current_cost = parseInt(initial_cost.textContent)
    current_cost += half_steamed_chicken_price
    initial_cost.textContent = current_cost
    checkout_button.style.display = 'block'
})

// for whole steamed chicken
const down_WSC = document.getElementById('decrease_WSC')
const up_WSC = document.getElementById('increase_WSC')
const WSC_quantity = document.getElementById('WSC_quantity')

down_WSC.addEventListener('click', function() {
    let current_WSC_quantity = parseInt(WSC_quantity.textContent)

    if (current_WSC_quantity > 0) {
        current_WSC_quantity -= 1
        WSC_quantity.textContent = current_WSC_quantity

        let current_cost = parseInt(initial_cost.textContent)
        current_cost -= whole_steamed_chicken_price
        initial_cost.textContent = current_cost

        if (current_cost == 0) {
            checkout_button.style.display ='none'
        }
    }
})

up_WSC.addEventListener('click', function() {
    let current_WSC_quantity = parseInt(WSC_quantity.textContent)
    current_WSC_quantity += 1
    WSC_quantity.textContent = current_WSC_quantity

    let current_cost = parseInt(initial_cost.textContent)
    current_cost += whole_steamed_chicken_price
    initial_cost.textContent = current_cost
    checkout_button.style.display = 'block'
})

// for pressing checkout and passing on hidden form

const hidden_form = document.getElementById('hidden_form')

checkout_button.addEventListener('click', function() {
    document.getElementById('SCR_quantity_input').value = SCR_quantity.textContent;
    document.getElementById('HSC_quantity_input').value = HSC_quantity.textContent;
    document.getElementById('WSC_quantity_input').value = WSC_quantity.textContent;
    document.getElementById('initial_cost_input').value = initial_cost.textContent;
    hidden_form.submit();
})