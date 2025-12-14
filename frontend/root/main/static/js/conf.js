export const Domains = {  // servers domains including ports
    'auth': 'http://127.0.0.1:8001/',
    'server': 'http://127.0.0.1:8002/',
}

export const Urls = {  // backend urls
    // authentication
    'registrationUrl': 'registration',
    'loginUrl': 'obtain',
    'logoutUrl': 'logout',
    'authStatusCheck': 'auth-check',

    // test
    'publickUrl': 'api/publick/',
    'secretUrl': 'api/secret/',

    // File System API
    getFileSystem: 'api/file-system/', // get folders & records
    FSRecords: 'api/file-system/records/', // post record
    FSRecord: (record_id) => `api/file-system/records/${record_id}/`, // patch/delete record
    FSFolders: 'api/file-system/folders/', // post folder
    FSFolder: (folder_id) => `api/file-system/folders/${folder_id}/`, // patch/delete folder

    // Move API
    moveBetween: 'api/file-system/move/between/',  // post - change objects order
    moveInside: 'api/file-system/move/inside/',  // post - put object in the new folder

    // Record API
    getRecordContent: (record_id) => `api/records/${record_id}/`, // get all record content
    notes: (record_id) => `api/records/${record_id}/notes/`, // post note
    note: (record_id, note_id) => `api/records/${record_id}/notes/${note_id}`, // get/patch/delete note
    images: (record_id) => `api/records/${record_id}/images/`, // post image
    image: (record_id, image_id) => `api/records/${record_id}/images/${image_id}/`, // get/delete image
    imagesGroups: (record_id) => `api/records/${record_id}/images-group/`, // post images group
    imagesGroup: (record_id, msg_id) => `api/records/${record_id}/images-group/${msg_id}/`, // get/delete images group
}

export const AJAX = {  // general implementation of AJAX requests
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

export const colors = {  // file system object colors mapping
    forward: {'white': 'w', 'green': 'g', 'blue': 'b', 'yellow': 'y', 'red': 'r'},
    revers: {'w': 'white', 'g': 'green', 'b': 'blue', 'y': 'yellow', 'r': 'red'},
}
