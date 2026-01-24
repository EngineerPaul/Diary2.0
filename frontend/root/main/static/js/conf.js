export const Domains = {  // servers domains including ports
    // for local and docker
    // 'auth': 'http://127.0.0.1:8001/',
    // 'server': 'http://127.0.0.1:8002/',
    // 'frontend': 'http://127.0.0.1:8000/',

    // for Nginx
    'auth': '/',
    'server': '/',
    'frontend': '/',
}

export const Urls = {  // backend urls
    // authentication
    'registrationUrl': 'auth/registration',
    'loginUrl': 'auth/obtain',
    'logoutUrl': 'auth/logout',
    'authStatusCheck': 'auth/auth-check',
    // TG Auth API
    tgAuthDate: 'auth/tg-auth/date',  // set tg auth date
    tgAuthCheck: 'auth/tg-auth/check', // get tg nickname

    // test
    'publickUrl': 'api/publick/',
    'secretUrl': 'api/secret/',

    // File System API (record)
    getFileSystem: 'api/file-system/record-content/', // get folders & records
    FSRecords: 'api/file-system/record-content/records/', // post record
    FSRecord: (record_id) => `api/file-system/record-content/records/${record_id}/`, // patch/delete record
    FSFolders: 'api/file-system/record-content/folders/', // post folder
    FSFolder: (folder_id) => `api/file-system/record-content/folders/${folder_id}/`, // patch/delete folder

    // File System API (notice)
    getFileSystemNotice: 'api/file-system/notice-content/', // get folders & notices
    FSNotices: 'api/file-system/notice-content/notices/', // post notice
    FSNotice: (notice_id) => `api/file-system/notice-content/notices/${notice_id}/`, // patch/delete notice
    FSFoldersNotice: 'api/file-system/notice-content/folders/', // post folder
    FSFolderNotice: (folder_id) => `api/file-system/notice-content/folders/${folder_id}/`, // patch/delete folder
    getNextDate: 'api/file-system/notice-content/get-nextdate/', // get nextdate in a periodic form

    // Move API
    moveBetween: 'api/file-system/move/between/',  // post - change objects order
    moveInside: 'api/file-system/move/inside/',  // post - put object in the new folder

    // Record API
    getRecordContent: (record_id) => `api/records/${record_id}/`, // get all record content
    notes: (record_id) => `api/records/${record_id}/notes/`, // post note
    note: (record_id, note_id) => `api/records/${record_id}/notes/${note_id}/`, // get/patch/delete note
    images: (record_id) => `api/records/${record_id}/images/`, // post image
    image: (record_id, image_id) => `api/records/${record_id}/images/${image_id}/`, // get/delete image
    imagesGroups: (record_id) => `api/records/${record_id}/images-group/`, // post images group
    imagesGroup: (record_id, msg_id) => `api/records/${record_id}/images-group/${msg_id}/`, // get/delete images group

    // Notice API
    noticeImages: (notice_id) => `api/notices/${notice_id}/images/`,  // get/post/delete images by notice
    noticeImage: (notice_id, img_id) => `api/notices/${notice_id}/images/${img_id}/`,  // get/delete single image by id
}

export const TelegramBot = {
    name: 'first2362bot',
    baseUrl: 'https://t.me/',
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
                // Logout и переадресация на страницу авторизации
                localStorage.setItem('IsLoggedIn', false)
                localStorage.removeItem('userInfo')
                
                // Обновление UI элементов, если они существуют
                const loginBTN = document.getElementById('loginBTN')
                const logoutBTN = document.getElementById('logoutBTN')
                if (loginBTN) loginBTN.style['display'] = 'inline-block'
                if (logoutBTN) logoutBTN.style['display'] = 'none'
                
                window.location.href = Domains['frontend'] + 'login'
                return Promise.reject(new Error(response.statusText))
            }
            if (response.status==403) {
                console.log("Error 403: no access rights")
                alert('Ошибка: у Вас недостаточно прав')
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
