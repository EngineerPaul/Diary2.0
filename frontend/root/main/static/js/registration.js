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

const sendRegistration = async function(event) {
    event.preventDefault()

    const regForm = document.getElementById('formRegistration')
    const userTimezone = Intl.DateTimeFormat().resolvedOptions().timeZone
    let data = {
        'username': regForm.username.value,
        'password': regForm.password.value,
        'timezone': userTimezone,
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
        
        // Извлекаем только известные поля из ответа
        const userInfo = {
            username: response.username,
            id: response.id,
            role: response.role,
            tg_nickname: null
        }
        
        logIn(userInfo)
        window.location.href = conf.Domains['frontend'] + ''
    }
}

const regForm = document.getElementById('formRegistration')
regForm.addEventListener('submit', sendRegistration)