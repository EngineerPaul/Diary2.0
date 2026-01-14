import * as conf from "./conf.js"


const loginBTN = document.getElementById('loginBTN')
const logoutBTN = document.getElementById('logoutBTN')


const logIn = function(userInfo) { // включение индикаторов авторизации
    localStorage.setItem('IsLoggedIn', true)
    localStorage.setItem('userInfo', JSON.stringify(userInfo))
    
    const username = userInfo.username
    console.log(`Username: ${username}`)
    loginBTN.style['display'] = 'none'
    logoutBTN.style['display'] = 'inline-block'
}

const logOut = async function() { // выключение индикаторов авторизации
    localStorage.setItem('IsLoggedIn', false)
    localStorage.removeItem('userInfo')

    loginBTN.style['display'] = 'inline-block'
    logoutBTN.style['display'] = 'none'
}

const sendAuthorization = async function(event) {
    event.preventDefault()

    // const authForm = document.getElementById('authorizationForm')
    let data = {
        'username': authForm.username.value,
        'password': authForm.password.value
    }
    const url = conf.Domains['auth'] + conf.Urls['loginUrl']
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
    console.log(response)

    if (response === undefined) {
        console.log(`Error: неопознанная ошибка авторизации`)
    } else {
        console.log(`Авторизация завершена`)
        
        const userInfo = {
            id: response.id,
            username: response.username,
            role: response.role,
            tg_nickname: response.tg_nickname
        }
        
        logIn(userInfo)
        window.location.href = conf.Domains['frontend'] + ''
    }
    
}

const authСheck = async function() {  // перенести на страницу login
    const url = conf.Domains['auth'] + conf.Urls['authStatusCheck']
    const options = {
        method: 'GET',
        headers: {'Content-Type': 'application/json'},
        credentials: 'include',
        // "X-CSRFToken": csrftoken,
        // mode: 'no-cors',
    }
    let response = await conf.AJAX.send(url, options)
    // console.log(response)  // {"success": bool, "right": bool}

    if (response) {
        if (response.right) {
            console.log(`Авторизация подтверждена`)
            console.log(response)
            logIn()
        }
        else {
            console.log(`Авторизация НЕ подтверждена`)
            logOut()
        }
    } else {
        console.log(`Ошибка сервера`)
    }
}

const authForm = document.getElementById('authorizationForm')
authForm.addEventListener('submit', sendAuthorization)
authСheck()
