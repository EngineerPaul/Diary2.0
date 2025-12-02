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


// ------------------------------------------------------
// Отправка картинок

  const domen = "http://127.0.0.1:8002/"
  const uploadUrl = "api/test-upload/"
  const form1 = document.getElementById('form1')
  const form2 = document.getElementById('form2')
  
  const sendForm = async function(event) {  // отправить 1 картинку на сервер (не работает)
    event.preventDefault()

    // const formData = new FormData(form1)  // FormData автоматически формирует корректный multipart/form-data‑запрос
    // FormData Автоматически собирает все поля формы, включая файл. Для файла сохраняются:
    // - имя (name из <input>),
    // - оригинальное имя файла (filename в запросе),
    // - MIME‑тип (type),
    // - содержимое.
    // FormData также сам устанавливает Content-Type: multipart/form-data; boundary=... с корректным boundary

    const formData = new FormData(form1) 
    const url = domen + uploadUrl
    const options = {
        method: 'POST',
        credentials: 'include',
        body: formData,
        // "X-CSRFToken": csrftoken,
        // mode: 'no-cors',
    }
    
    let response = await conf.AJAX.send(url, options)
    console.log(response)

    if (response === undefined) {
        console.log(`Error: неопознанная ошибка`)
    } else {
        console.log(`запрос отправлен`)
    }

  }
  form1.addEventListener('submit', sendForm)

  const checkImgSize = function(files) {  // Проверка размеров файлов

    const maxSize = 5 * 1024 * 1024  // 5 MB
    const maxTotalSize = maxSize * 10

    // Проверка каждого файла
    let totalSize = 0
    for (const file of files) {
        if (file.size > maxSize) {
            console.error(`Файл "${file.name}" превышает лимит ${maxSize / 1024 / 1024} MB`)
            alert(`Файл "${file.name}" слишком большой. Максимум: 5 MB`)
            return false
        }
        totalSize += file.size
    }
    
    // Проверка общего размера
    if (totalSize > maxTotalSize) {
        console.error(`Общий размер файлов превышает ${maxTotalSize / 1024 / 1024} MB`)
        alert(`Общий размер файлов слишком большой. Максимум: 20 MB`)
        return false
    }
    return true
  }

  const sendForm2 = async function(event) {  // отправить несколько картинок на сервер 
    event.preventDefault()

    const files = form2.img_input2.files
    if (!checkImgSize(files)) return

    const formData = new FormData(form2) 
    const url = domen + uploadUrl
    const options = {
        method: 'POST',
        credentials: 'include',
        body: formData,
    }
    
    await fetch(url, options)
      .then(response => {
        if (!response.ok) {
          throw new Error(`Error: ошибка отправки картинки ${response.status}`)
        }
        return response.json()
      })
      .then(data => {
        // обновить данные страницы
        console.log('Данные отправлены', data)
      })
      .catch(error => {
        console.log('Error', error)
      })

  }
  form2.addEventListener('submit', sendForm2)
