// default constants
const steamed_chicken_rice_price = 5;
const half_steamed_chicken_price = 15;
const whole_steamed_chicken_price = 20;

// total cost b4 gst and allat
const initial_cost = document.querySelector('#initial_cost')
const checkout_button = document.querySelector('#checkout_icon')
const checkout_area = document.querySelector('#checkout_area')
const flying_scr = document.querySelector('.flying_scr')
const flying_hsc = document.querySelector('.flying_hsc')
const flying_wsc = document.querySelector('.flying_wsc')


// for steamed chicken rice
const down_SCR = document.querySelector('#decrease_SCR')
const up_SCR = document.querySelector('#increase_SCR')
const SCR_quantity = document.querySelector('#SCR_quantity')

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
    checkout_area.style.border = '4px solid #ff3131'
    setTimeout(() => {
        checkout_area.style.border = '2px solid grey';
    }, 900);
    SCR_quantity.textContent = current_SCR_quantity

    let current_cost = parseInt(initial_cost.textContent)
    current_cost += steamed_chicken_rice_price
    initial_cost.textContent = current_cost
    checkout_button.style.display = 'block'

    flying_scr.classList.add('fly_in');
    setTimeout(function() {
        flying_scr.classList.remove('fly_in');
    }, 1000)
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
    checkout_area.style.border = '4px solid #ff3131'
    setTimeout(() => {
        checkout_area.style.border = '2px solid grey';
    }, 900);
    HSC_quantity.textContent = current_HSC_quantity

    let current_cost = parseInt(initial_cost.textContent)
    current_cost += half_steamed_chicken_price
    initial_cost.textContent = current_cost
    checkout_button.style.display = 'block'

    flying_hsc.classList.add('fly_in');
    setTimeout(function() {
        flying_hsc.classList.remove('fly_in');
    }, 1000)

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
    checkout_area.style.border = '4px solid #ff3131'
    setTimeout(() => {
        checkout_area.style.border = '2px solid grey';
    }, 900);
    WSC_quantity.textContent = current_WSC_quantity

    let current_cost = parseInt(initial_cost.textContent)
    current_cost += whole_steamed_chicken_price
    initial_cost.textContent = current_cost
    checkout_button.style.display = 'block'

    flying_wsc.classList.add('fly_in');
    setTimeout(function() {
        flying_wsc.classList.remove('fly_in');
    }, 1000)
})

// for pressing checkout and passing on hidden form

const hidden_form = document.getElementById('hidden_form')

checkout_button.addEventListener('click', function() {
    document.getElementById('SCR_quantity_input').value = SCR_quantity.textContent;
    document.getElementById('HSC_quantity_input').value = HSC_quantity.textContent;
    document.getElementById('WSC_quantity_input').value = WSC_quantity.textContent;
    document.getElementById('initial_cost_input').value = initial_cost.textContent;
    checkout_button.classList.toggle('grow');
    hidden_form.submit();
})