// default constants
const steamed_chicken_rice_price = 5;
const half_steamed_chicken_price = 15;
const whole_steamed_chicken_price = 20;

// total cost b4 gst and allat
const initial_cost = document.getElementById('initial_cost')

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
    }
})

up_SCR.addEventListener('click', function() {
    let current_SCR_quantity = parseInt(SCR_quantity.textContent)
    current_SCR_quantity += 1
    SCR_quantity.textContent = current_SCR_quantity

    let current_cost = parseInt(initial_cost.textContent)
    current_cost += steamed_chicken_rice_price
    initial_cost.textContent = current_cost
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
    }
})

up_HSC.addEventListener('click', function() {
    let current_HSC_quantity = parseInt(HSC_quantity.textContent)
    current_HSC_quantity += 1
    HSC_quantity.textContent = current_HSC_quantity

    let current_cost = parseInt(initial_cost.textContent)
    current_cost += half_steamed_chicken_price
    initial_cost.textContent = current_cost
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
    }
})

up_WSC.addEventListener('click', function() {
    let current_WSC_quantity = parseInt(WSC_quantity.textContent)
    current_WSC_quantity += 1
    WSC_quantity.textContent = current_WSC_quantity

    let current_cost = parseInt(initial_cost.textContent)
    current_cost += whole_steamed_chicken_price
    initial_cost.textContent = current_cost
})

// for pressing checkout and passing on hidden form