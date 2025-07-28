// if owner requests, can add a phone number requirement for customers

const hawker_button = document.querySelector('#hawker_login_button')
const enter_id = document.querySelector('#enter_hawker_id')

hawker_button.addEventListener('click', function() {
    enter_id.classList.add('appear');
})