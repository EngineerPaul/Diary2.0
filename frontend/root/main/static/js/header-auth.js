import * as conf from "./conf.js";

const loginBTN = document.getElementById('loginBTN')
const logoutBTN = document.getElementById('logoutBTN')

if (JSON.parse(localStorage.getItem('IsLoggedIn'))) {
    loginBTN.style['display'] = 'none'
    logoutBTN.style['display'] = 'inline-block'
}
else {
    loginBTN.style['display'] = 'inline-block'
    logoutBTN.style['display'] = 'none'
}


const exit = async function() {
    await sendLogOut()
    logOut() // индикаторы
    console.log('Выход из профиля')
}
const sendLogOut = async function() {
    const url = conf.Domains['auth'] + conf.Urls['logoutUrl']
    const options = {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
        },
        credentials: 'include',
    }
    const response = await conf.AJAX.send(url, options)

    if (response === undefined) {
        console.log(`Error: неопознанная ошибка`)
    } else if (response.success) {
        console.log(`Выход завершен`)
    }
}
const logOut = async function() { // выключение индикаторов авторизации
    // mark.style['background-color'] = 'darkkhaki'
    // mark.innerHTML = 'Не авторизован'
    localStorage.setItem('IsLoggedIn', false)
    localStorage.removeItem('userInfo')

    const loginBTN = document.getElementById('loginBtn')
    const logoutBTN = document.getElementById('logoutBTN')

    loginBTN.style['display'] = 'inline-block'
    logoutBTN.style['display'] = 'none'

}

logoutBTN.addEventListener('click', exit)
