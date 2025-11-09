import * as conf from "./conf.js"


const loginBTN = document.getElementById('loginBTN')
const logoutBTN = document.getElementById('logoutBTN')


const logIn = function(username) { // включение индикаторов авторизации
    localStorage.setItem('IsLoggedIn', true)
    
    if (username) {
        localStorage.setItem('username', username)
    } else {
        username = localStorage.getItem('username')
    }
    console.log(`Username: ${username}`)
    loginBTN.style['display'] = 'none'
    logoutBTN.style['display'] = 'inline-block'
}

const sendRegistration = async function(event) {
    event.preventDefault()

    const regForm = document.getElementById('formRegistration')
    let data = {
        'username': regForm.username.value,
        'password': regForm.password.value
    }
    const url = conf.Domains['auth'] + conf.Urls['registrationUrl']
    const options = {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        credentials: 'include',
        body: JSON.stringify(data),
        // "X-CSRFToken": csrftoken,
        // mode: 'no-cors',
    }
    let response = await conf.AJAX.send(url, options)
    // console.log(response)

    if (response === undefined) {
        console.log(`Error: неопознанная ошибка регистрации`)
        console.log(response)
    } else if (response.success == false) {
        console.log(response)
        console.log(`Ошшибка запроса: ${JSON.stringify(response.error)}`)
    } else {
        console.log(`Регистрация завершена. Username=${data['username']}`)
        logIn(data['username'])
    }
}

const regForm = document.getElementById('formRegistration')
regForm.addEventListener('submit', sendRegistration)