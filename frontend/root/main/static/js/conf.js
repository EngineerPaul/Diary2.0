export const Domains = {
    'auth': 'http://127.0.0.1:8001/',
    'server': 'http://127.0.0.1:8002/',
}

export const Urls = {
    'registrationUrl': 'registration',
    'loginUrl': 'obtain',
    'logoutUrl': 'logout',
    'authStatusCheck': 'auth-check',

    'publickUrl': 'publick',  // server doesn't exist
    'secretUrl': 'secret',  // server doesn't exist
}

export const AJAX = {
    send: async function(url, options) { // формируется запрос на url с options
        try {
            let response = await fetch(url, options)
            let data = await this.check_status(response).catch(this.raise_error)

            if (data) {
                let jsonData = this.to_json(data)
                return jsonData
            }

        } catch (error) {
            console.log('Error: неизвестная ошибка catch')
            // console.log(error.message)
        }

    },
    check_status: function(response) { // проверка статус кода запроса
        if (!response.ok) {
            if (response.status==401) {
                console.log("Error 401: credentials not valid")
            }
            if (response.status==403) {
                console.log("Error 403: no access rights")
            }
            if (![401, 403].includes(response.status)) {  // если не
                console.log(`Error ${response.status}`)
            }
            return Promise.reject(new Error(response.statusText))
        }
        return Promise.resolve(response)
    },
    to_json: function(response) { // десериализация строки в json объект
        return response.json()
    },
    raise_error: function(error) { // обработка ошибок (400е и 500е статусы не являются ошибками)
        // console.log('Error: raise_error. ', error)
    },
}