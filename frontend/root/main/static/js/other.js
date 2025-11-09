// test buttons
import * as conf from "./conf.js"

const getPublick = async function() {
    const url = conf.Domains['server'] + conf.Urls['publickUrl']
    let headers = {
        'Content-Type': 'application/json',
    }
    const options = {
        method: 'GET',
        headers: headers,
        credentials: 'include',
        // "X-CSRFToken": csrftoken,
        // mode: 'no-cors',
    }
    let response = await conf.AJAX.send(url, options)
    console.log(response)

    if (response) {
        console.log(`Ответ сервера: ${JSON.stringify(response, null, 1)}`)
    } else {
        console.log(`Ошибка сервера`)
    }
}
const getLatent = async function() {
    const url = conf.Domains['server'] + conf.Urls['secretUrl']
    let headers = {
        'Content-Type': 'application/json',
    }
    const options = {
        method: 'GET',
        headers: headers,
        credentials: 'include',
        // "X-CSRFToken": csrftoken,
        // mode: 'no-cors',
    }
    let response = await conf.AJAX.send(url, options)

    console.log('response', response)

    if (response) {
        console.log(`Ответ сервера: ${JSON.stringify(response, null, 1)}`)
    } else {
        console.log(`Ошибка сервера`)
    }
}

const testPublic = document.getElementById('testPublic')
const testSecret = document.getElementById('testSecret')
testPublic.addEventListener('click', getPublick)
testSecret.addEventListener('click', getLatent)
