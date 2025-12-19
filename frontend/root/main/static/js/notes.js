import * as conf from "./conf.js";

let slider = {
    shiftLeft: function(slider, imageArea) {  // shift images left
        let leftSliderBorder = slider.getBoundingClientRect().left
        let childrenArea = imageArea.children
        let nextElem = null
        for (let i=childrenArea.length-1; i >= 0; i--) {
            if (childrenArea[i].getBoundingClientRect().left < leftSliderBorder) {
                nextElem = childrenArea[i]
                break
            }
        }
        if (!nextElem) return

        let leftImageBorder = nextElem.getBoundingClientRect().left
        let currentShift = imageArea.style.left.slice(0,-2)
        imageArea.style.left = currentShift - Math.floor(leftImageBorder-leftSliderBorder) + 'px'
    },
    shiftRight: function(slider, imageArea) {  // shift images right
        let rightSliderBorder = slider.getBoundingClientRect().right
        let childrenArea = imageArea.children
        let nextElem = null
        for (let i=0; i < childrenArea.length; i++) {
            if (childrenArea[i].getBoundingClientRect().right > rightSliderBorder) {
                nextElem = childrenArea[i]
                break
            }
        }
        if (!nextElem) return

        let rightImageBorder = nextElem.getBoundingClientRect().right
        let currentShift = imageArea.style.left.slice(0,-2)
        imageArea.style.left = currentShift - Math.ceil(rightImageBorder-rightSliderBorder) + 'px'
    },
    shiftSlider: function(event) {  // shift images into the slider
        let shiftButton = event.target.closest('.rectangle')
        if (!shiftButton) return false
        let images = shiftButton.closest('.images')
        let slider = images.querySelector('.slider')
        let imageArea = images.querySelector('.image-area')

        let direction = shiftButton.dataset['direction']
        if (direction === 'right') {
            this.shiftRight(slider, imageArea)
        } else if (direction === 'left') {
            this.shiftLeft(slider, imageArea)
        } else {
            console.log('Error: getSlider()')
        }
    },
    run: function() {
        document.addEventListener('click', this.shiftSlider.bind(this))
    }
}
slider.run()

let queries = {
    recordId: null, // id of whole record

    getRecordId: function() { // getting record id from the url
        // Извлекаем ID из URL (например, /notes/19/ -> 19)
        const pathname = window.location.pathname
        const match = pathname.match(/\/notes\/(\d+)\//)
        if (match && match[1]) {
            return parseInt(match[1], 10)
        }
        // Если ID не найден, возвращаем null или выбрасываем ошибку
        console.error('Error: record ID not found in URL')
        return null
    },
    getContent: async function() { // getting record content from server
        const url = conf.Domains['server'] + conf.Urls.getRecordContent(this.recordId)
        const options = {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
            },
            credentials: 'include',
        }
        const response = await conf.AJAX.send(url, options)

        if (response === undefined) {
            console.log(`Error: неопознанная ошибка при получении контента записи`)
            return null
        }

        if (!response.record || !response.messages) {
            console.log(`Error: некорректный формат ответа от сервера`)
            return null
        }
        console.log(response)

        const recordDetail = response.record
        const messages = response.messages


        return response
    },
    createNote: async function(text) { // send creation note form to server
        const url = conf.Domains['server'] + conf.Urls.notes(this.recordId)
        const options = {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            credentials: 'include',
            body: JSON.stringify({
                text: text
            })
        }
        const response = await conf.AJAX.send(url, options)
        return response
    },
    createImages: async function(files) { // send creation image group form to server
        const url = conf.Domains['server'] + conf.Urls.imagesGroups(this.recordId)
        const formData = new FormData()
        
        // Добавляем каждый файл в FormData с одинаковым ключом 'file' для Django
        for (let i = 0; i < files.length; i++) {
            formData.append('file', files[i])
        }
        
        const options = {
            method: 'POST',
            credentials: 'include',
            body: formData
        }
        const response = await conf.AJAX.send(url, options)
        return response
    },
    editImagesGroup: async function(msgId, files) { // add images to existing images group
        const url = conf.Domains['server'] + conf.Urls.images(this.recordId)
        const formData = new FormData()
        
        formData.append('msg_id', msgId)
        for (let i = 0; i < files.length; i++) {
            formData.append('file', files[i])
        }
        
        const options = {
            method: 'POST',
            credentials: 'include',
            body: formData
        }
        const response = await conf.AJAX.send(url, options)
        return response
    },
    updateNote: async function(noteId, text) { // change any comment
        const url = conf.Domains['server'] + conf.Urls.note(this.recordId, noteId)
        const options = {
            method: 'PATCH',
            headers: {
                'Content-Type': 'application/json',
            },
            credentials: 'include',
            body: JSON.stringify({
                text: text
            })
        }
        const response = await conf.AJAX.send(url, options)
        return response
    },
    updateRecord: async function(title, description, color) { // change record (settings and theme)
        const url = conf.Domains['server'] + conf.Urls.FSRecord(this.recordId)
        const options = {
            method: 'PATCH',
            headers: {
                'Content-Type': 'application/json',
            },
            credentials: 'include',
            body: JSON.stringify({
                title: title,
                description: description || '',
                color: conf.colors.forward[color] || 'w'
            })
        }
        const response = await conf.AJAX.send(url, options)
        return response
    },
    handleUpdateRecordSubmit: async function(event) {  // record update submit event
        event.preventDefault()
        const nameInput = document.getElementById('fNoteName')
        const contentTextarea = document.getElementById('fNoteContent')
        const markerInput = document.querySelector('#modalRecord input[name="marker"]:checked')
        
        if (!nameInput) {
            console.log('Error: поле названия не найдено')
            return
        }
        
        const title = nameInput.value.trim()
        if (!title) {
            console.log('Error: название не может быть пустым')
            return
        }
        
        const description = contentTextarea ? contentTextarea.value.trim() : ''
        const color = markerInput ? markerInput.value : 'white'
        
        const response = await this.updateRecord(title, description, color)
        if (response) {
            if (settings && settings.modalBlock) {
                settings.modalBlock.style.display = 'none'
            }
            
            await content.getContent()
            content.viewContent()
        }
    },
    delNote: async function(noteId) { // delete any note
        const url = conf.Domains['server'] + conf.Urls.note(this.recordId, noteId)
        const options = {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json',
            },
            credentials: 'include',
        }
        const response = await conf.AJAX.send(url, options)
        return response
    },
    delImage: async function(imageId) { // delete any single image
        const url = conf.Domains['server'] + conf.Urls.image(this.recordId, imageId)
        const options = {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json',
            },
            credentials: 'include',
        }
        const response = await conf.AJAX.send(url, options)
        return response
    },
    delImages: async function(msgId) { // delete any images group
        const url = conf.Domains['server'] + conf.Urls.imagesGroup(this.recordId, msgId)
        const options = {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json',
            },
            credentials: 'include',
        }
        const response = await conf.AJAX.send(url, options)
        return response
    },
    delRecord: function() { // delete whole record with all notes and images

    },
    handleAddNoteSubmit: async function(event) {
        event.preventDefault()
        const textarea = document.getElementById('fNoteText')
        const text = textarea.value.trim()
        
        if (!text) {
            console.log('Error: текст заметки не может быть пустым')
            return
        }
        
        const response = await this.createNote(text)
        if (response) {

            if (settings && settings.modalBlock) {
                settings.modalBlock.style.display = 'none'
            }

            textarea.value = ''
            
            await content.getContent()
            content.viewContent()
        }
    },
    handleAddImagesSubmit: async function(event) {
        event.preventDefault()
        const fileInput = document.getElementById('fImages')
        const files = fileInput.files
        
        if (!files || files.length === 0) {
            console.log('Error: необходимо выбрать хотя бы один файл')
            return
        }
        
        let response
        // Проверяем data-атрибут формы для редактирования существующей группы изображений
        const form = event.target
        const editMsgId = form.dataset.editMsgId
        if (editMsgId) {
            response = await this.editImagesGroup(Number(editMsgId), files)
            delete form.dataset.editMsgId // Удаляем data-атрибут после использования
        } else {
            // Создаем новую группу изображений
            response = await this.createImages(files)
        }
        
        if (response) {
            if (settings && settings.modalBlock) {
                settings.modalBlock.style.display = 'none'
            }
            
            fileInput.value = ''
            const fileInputButton = document.querySelector('.file-input-button')
            if (fileInputButton) {
                fileInputButton.textContent = 'Выберите файл'
            }
            
            await content.getContent()
            content.viewContent()
        }
    },
    run: function() {
        this.recordId = this.getRecordId()
        
        const addNoteForm = document.getElementById('addNoteForm')
        const addImagesForm = document.getElementById('addImagesForm')
        const updateRecordForm = document.getElementById('crtRecordForm')
        addNoteForm.addEventListener('submit', this.handleAddNoteSubmit.bind(this))
        addImagesForm.addEventListener('submit', this.handleAddImagesSubmit.bind(this))
        updateRecordForm.addEventListener('submit', this.handleUpdateRecordSubmit.bind(this))
    }
}
queries.run()

let content = {
    theme: null, // title of whole record
    description: null, // record rescription
    color: null,  // record color
    messages: {},  // content

    getContent: async function() { // parsing data (details and messages) from server
        const {messages: messages, record: recordDetail} = await queries.getContent()
        // recordDetail - {record_id: 19, user_id: 1, title: 'record 1'} позже добавится description
        this.theme = recordDetail.title
        this.description = recordDetail.description
        this.color = recordDetail.color ? conf.colors.revers[recordDetail.color] : 'white'
        this.messages = messages
    },

    editNote: async function(noteId) {  // event of update note by pencil

        const record = document.querySelector(`.record[id="${noteId}"]`)
        if (!record) {
            console.log('Error: заметка не найдена')
            return
        }
        
        const recordText = record.querySelector('.record-text')
        const textarea = recordText ? recordText.querySelector('.record-text-edit') : null
        if (!textarea) {
            console.log('Error: форма редактирования не найдена')
            return
        }
        const text = textarea.value.trim()
        if (!text) {
            console.log('Error: текст не может быть пустым')
            return
        }

        // Проверяем, изменился ли текст
        const noteIndex = this.messages.findIndex(msg => 
            msg.type === 'note' && msg.note_id === noteId
        )
        const originalText = noteIndex !== -1 ? this.messages[noteIndex].text : ''
        
        // Если текст не изменился, просто обновляем UI без запроса на сервер
        if (originalText === text) {
            this._updateNoteUI(record, recordText, text)
            return
        }

        const response = await queries.updateNote(noteId, text)
        
        if (response) {
            this._updateNoteUI(record, recordText, text)
            
            // Обновляем данные в content.messages
            if (noteIndex !== -1) {
                this.messages[noteIndex].text = text
            }
        }
    },
    _updateNoteUI: function(record, recordText, text) {  // disable note edit mode
        // Обновляем текст в DOM
        recordText.innerHTML = ''
        recordText.textContent = text
        
        // Скрываем галочку после сохранения
        const recordHeader = record.querySelector('.record-header')
        if (recordHeader) {
            const checkmark = recordHeader.querySelector('.checkmark')
            const editElement = recordHeader.querySelector('.edit')
            if (checkmark) {
                checkmark.style.display = 'none'
            }
            if (editElement) {
                editElement.style.marginLeft = 'auto'
            }
        }
    },

    delContent: function(event) { // event of deletion any type content by cross
        // image cross
        let imageCross = event.target.closest('.image-cross')
        if (imageCross) {
            let image = imageCross.closest('.image')
            if (image) {
                let img = image.querySelector('img')
                if (img && img.id) {
                    let imagesBlock = imageCross.closest('.images')
                    if (imagesBlock && imagesBlock.id) {
                        this.delImage(Number(img.id), Number(imagesBlock.id))
                        return
                    }
                }
            }
        }
        
        // images or record cross
        let cross = event.target.closest('.cross')
        if (!cross) return
        let record = cross.closest('.record')
        let images = cross.closest('.images')
        if (record) this.delNote(record.id)
        if (images) this.delImages(images.id)
    },
    delNote: async function(recordId) { // event of deletion any note
        const noteIdNum = Number(recordId)
        this.messages = this.messages.filter(msg => {
            if (msg.type === 'note' && msg.note_id === noteIdNum) {
                return false
            }
            return true
        })
        await queries.delNote(noteIdNum)
        this.viewContent()
    },
    delImage: async function(imageId, msgId) { // event of deletion any single image
        const imageIdNum = Number(imageId)
        const msgIdNum = Number(msgId)
        
        let imagesGroup = null
        let groupIndex = -1
        for (let i = 0; i < this.messages.length; i++) {
            if (this.messages[i].type === 'images' && this.messages[i].msg_id === msgIdNum) {
                imagesGroup = this.messages[i]
                groupIndex = i
                break
            }
        }
        
        if (!imagesGroup || !imagesGroup.images) {
            console.log('Error: группа изображений не найдена')
            return
        }
        
        const imageIndex = imagesGroup.images.findIndex(img => img.image_id === imageIdNum)
        if (imageIndex !== -1) {
            imagesGroup.images.splice(imageIndex, 1)
        }

        if (imagesGroup.images.length === 0 && groupIndex !== -1) {
            this.messages.splice(groupIndex, 1)
        }
        
        await queries.delImage(imageIdNum)
        this.viewContent()
    },
    updateSliderHeight: function(slider) { // change slider height using the heighter image
        if (!slider) return
        
        let imageArea = slider.querySelector('.image-area')
        if (!imageArea) return
        
        let images = imageArea.querySelectorAll('.image')
        if (images.length === 0) return
        
        // Находим самую высокую картинку
        let maxHeight = 0
        for (let j = 0; j < images.length; j++) {
            let img = images[j].querySelector('img')
            if (img) {
                let imgHeight = img.offsetHeight || img.naturalHeight || 0
                if (imgHeight > maxHeight) {
                    maxHeight = imgHeight
                }
            }
        }
        
        // Устанавливаем высоту блока на основе самой высокой картинки (не выше 300 css)
        if (maxHeight > 0) {
            slider.style.height = Math.min(maxHeight, 300) + 'px'
        }
    },
    updateImagesBlockHeight: function() { // пересчет высоты всех блоков изображений на основе самой высокой картинки
        let imagesBlocks = document.querySelectorAll('.images')
        for (let i = 0; i < imagesBlocks.length; i++) {
            let slider = imagesBlocks[i].querySelector('.slider')
            this.updateSliderHeight(slider)
        }
    },
    delImages: async function(msgId) { // event of deletion any image group (with images)
        const msgIdNum = Number(msgId)
        this.messages = this.messages.filter(msg => {
            if (msg.type === 'images' && msg.msg_id === msgIdNum) {
                return false
            }
            return true
        })
        await queries.delImages(msgIdNum)
        this.viewContent()
    },

    viewContent: function() { // display messages by msg type
        const themeElement = document.querySelector('.theme')
        if (themeElement && this.theme) {
            themeElement.textContent = this.theme
        }
        const descriptionElement = document.getElementById('description')
        if (descriptionElement) {
            descriptionElement.textContent = this.description || ''
        }
        
        let content = document.getElementById('content')
        content.innerHTML = ''
        for (let i=0; i<this.messages.length; i++) {
            if (this.messages[i].type === 'note') {
                this.viewNote(this.messages[i])
            } else if (this.messages[i].type === 'images') {
                this.viewImages(this.messages[i])
            } else {
                console.log('Error: message type is incorrect')
            }
        }
    },
    viewNote: function(noteData) { // display a note block from messages data
        let content = document.getElementById('content')
        let record = this.createElement({
            tag: 'div',
            classList: ['record'],
            parent: content,
            params: {id: noteData.note_id},
        })
        let recordHeader = this.createElement({
            tag: 'div',
            classList: ['record-header'],
            parent: record,
            params: {},
        })
        const noteDate = noteData.changed_at ? new Date(noteData.changed_at) : "error"
        let dateString = noteDate.toLocaleDateString('ru-RU', {
            year: 'numeric',
            month: '2-digit',
            day: '2-digit',
            hour: '2-digit',
            minute: '2-digit'
        })
        let date = this.createElement({
            tag: 'div',
            classList: ['date'],
            parent: recordHeader,
            params: {textContent: dateString},
        })
        let edit = this.createSVG({
            parent: recordHeader,
            className: 'edit',
            viewBox: '0 0 24 24',
            pathLst: [
                'M1.172,19.119A4,4,0,0,0,0,21.947V24H2.053a4,4,0,0,0,2.828-1.172L18.224,9.485,14.515,5.776Z',
                'M23.145.855a2.622,2.622,0,0,0-3.71,0L15.929,4.362l3.709,3.709,3.507-3.506A2.622,2.622,0,0,0,23.145.855Z'
            ],
        })
        let cross = this.createSVG({
            parent: recordHeader,
            className: 'cross',
            viewBox: '0 0 512.021 512.021',
            pathLst: ['M301.258,256.01L502.645,54.645c12.501-12.501,12.501-32.769,0-45.269c-12.501-12.501-32.769-12.501-45.269,0l0,0   L256.01,210.762L54.645,9.376c-12.501-12.501-32.769-12.501-45.269,0s-12.501,32.769,0,45.269L210.762,256.01L9.376,457.376   c-12.501,12.501-12.501,32.769,0,45.269s32.769,12.501,45.269,0L256.01,301.258l201.365,201.387   c12.501,12.501,32.769,12.501,45.269,0c12.501-12.501,12.501-32.769,0-45.269L301.258,256.01z'],
        })
        let hr = this.createElement({
            tag: 'hr',
            classList: [],
            parent: record,
            params: {},
        })
        let recordText = this.createElement({
            tag: 'div',
            classList: ['record-text'],
            parent: record,
            params: {textContent: noteData.text},
        })
    },
    viewImages: function(imagesData) { // display an images block from messages data
        let content = document.getElementById('content')
        let images = this.createElement({
            tag: 'div',
            classList: ['images'],
            parent: content,
            params: {id: imagesData.msg_id},
        })

        let sliderDirecrionLeft = this.createElement({
            tag: 'div',
            classList: ['slide-direction'],
            parent: images,
            params: {},
        })
        let rectangleLeft = this.createElement({
            tag: 'div',
            classList: ['rectangle'],
            parent: sliderDirecrionLeft,
            params: {},
        })
        rectangleLeft['dataset']['direction'] = 'left'
        let svgLeft = this.createSVG({
            parent: rectangleLeft,
            className: '',
            viewBox: '0 0 24 24',
            pathLst: ['M17.921,1.505a1.5,1.5,0,0,1-.44,1.06L9.809,10.237a2.5,2.5,0,0,0,0,3.536l7.662,7.662a1.5,1.5,0,0,1-2.121,2.121L7.688,15.9a5.506,5.506,0,0,1,0-7.779L15.36.444a1.5,1.5,0,0,1,2.561,1.061Z'],
        })

        let slider = this.createElement({
            tag: 'div',
            classList: ['slider'],
            parent: images,
            params: {},
        })
        // Скрываем блок до загрузки всех изображений
        slider.style.opacity = '0'
        let imageArea = this.createElement({
            tag: 'div',
            classList: ['image-area'],
            parent: slider,
            params: {},
        })
        let imagesList = imagesData.images
        let loadedImagesCount = 0
        let totalImagesCount = imagesList.length
        let allImagesLoaded = false
        
        // Функция для установки высоты и показа блока
        const showSlider = () => {
            if (!allImagesLoaded) {
                allImagesLoaded = true
                this.updateSliderHeight(slider)
                // Показываем блок с плавным переходом
                slider.style.transition = 'opacity 0.2s ease-in'
                slider.style.opacity = '1'
            }
        }
        
        for (let i=0; i<imagesList.length; i++) {
            let image = this.createElement({
                tag: 'div',
                classList: ['image'],
                parent: imageArea,
                params: {},
            })
            let img = this.createElement({
                tag: 'img',
                classList: [],
                parent: image,
                params: {src: imagesList[i].url, id: imagesList[i].image_id},
            })
            let imageCross = this.createSVG({
                parent: image,
                className: 'image-cross',
                viewBox: '0 0 512.021 512.021',
                pathLst: ['M301.258,256.01L502.645,54.645c12.501-12.501,12.501-32.769,0-45.269c-12.501-12.501-32.769-12.501-45.269,0l0,0   L256.01,210.762L54.645,9.376c-12.501-12.501-32.769-12.501-45.269,0s-12.501,32.769,0,45.269L210.762,256.01L9.376,457.376   c-12.501,12.501-12.501,32.769,0,45.269s32.769,12.501,45.269,0L256.01,301.258l201.365,201.387   c12.501,12.501,32.769,12.501,45.269,0c12.501-12.501,12.501-32.769,0-45.269L301.258,256.01z'],
            })
            
            // Добавляем обработчик загрузки изображения для пересчета высоты
            img.addEventListener('load', () => {
                loadedImagesCount++
                if (loadedImagesCount === totalImagesCount) {
                    // Все изображения загружены
                    showSlider()
                }
            })
            
            // Если изображение уже загружено (из кэша), сразу увеличиваем счетчик
            if (img.complete) {
                loadedImagesCount++
                if (loadedImagesCount === totalImagesCount) {
                    showSlider()
                }
            }
        }
        let editor = this.createSVG({
            parent: images,
            className: 'editor',
            viewBox: '0 0 24 24',
            pathLst: [
                'M1.172,19.119A4,4,0,0,0,0,21.947V24H2.053a4,4,0,0,0,2.828-1.172L18.224,9.485,14.515,5.776Z',
                'M23.145.855a2.622,2.622,0,0,0-3.71,0L15.929,4.362l3.709,3.709,3.507-3.506A2.622,2.622,0,0,0,23.145.855Z'
            ],
        })
        let cross = this.createSVG({
            parent: images,
            className: 'cross',
            viewBox: '0 0 512.021 512.021',
            pathLst: ['M301.258,256.01L502.645,54.645c12.501-12.501,12.501-32.769,0-45.269c-12.501-12.501-32.769-12.501-45.269,0l0,0   L256.01,210.762L54.645,9.376c-12.501-12.501-32.769-12.501-45.269,0s-12.501,32.769,0,45.269L210.762,256.01L9.376,457.376   c-12.501,12.501-12.501,32.769,0,45.269s32.769,12.501,45.269,0L256.01,301.258l201.365,201.387   c12.501,12.501,32.769,12.501,45.269,0c12.501-12.501,12.501-32.769,0-45.269L301.258,256.01z'],
        })
        let sliderDirecrionRight = this.createElement({
            tag: 'div',
            classList: ['slide-direction'],
            parent: images,
            params: {},
        })
        let rectangleRight = this.createElement({
            tag: 'div',
            classList: ['rectangle'],
            parent: sliderDirecrionRight,
            params: {},
        })
        rectangleRight.dataset['direction'] = 'right'
        let svgRight = this.createSVG({
            parent: rectangleRight,
            className: '',
            viewBox: '0 0 24 24',
            pathLst: ['M6.079,22.5a1.5,1.5,0,0,1,.44-1.06l7.672-7.672a2.5,2.5,0,0,0,0-3.536L6.529,2.565A1.5,1.5,0,0,1,8.65.444l7.662,7.661a5.506,5.506,0,0,1,0,7.779L8.64,23.556A1.5,1.5,0,0,1,6.079,22.5Z'],
        })
    },
    createElement: function(options) { // create usual HTML elem
        // options: {tag, classList, parent, params}
        let element = document.createElement(options.tag)
        if (options.classList) {
            for (let i=0; i<options.classList.length; i++) {
                element.classList.add(options.classList[i])
            }
        }
        if (options.params) {
            for (let param of Object.keys(options.params)) {
                element[param] = options.params[param]
            }
        }
        options.parent.appendChild(element)
        return element
    },
    createSVG: function(options) { // create usual HTML svg elem
        // options: {parent, className, viewBox, pathLst}
        let svg = document.createElementNS("http://www.w3.org/2000/svg", "svg")
        svg.setAttributeNS(null, 'class', options.className)
        svg.setAttributeNS(null, 'viewBox', options.viewBox)
        for (let i=0; i < options.pathLst.length; i++) {
            let svgPath = document.createElementNS("http://www.w3.org/2000/svg", 'path')
            svgPath.setAttributeNS(null, 'd', options.pathLst[i])
            svg.appendChild(svgPath)
        }
        options.parent.append(svg)
        return svg
        // https://ru.stackoverflow.com/questions/1123250/%D0%9A%D0%B0%D0%BA-%D0%B2%D1%81%D1%82%D0%B0%D0%B2%D0%B8%D1%82%D1%8C-svg-%D0%BA%D0%BE%D0%B4-%D0%BD%D0%B0-%D1%81%D0%B0%D0%B9%D1%82-%D1%81-%D0%BF%D0%BE%D0%BC%D0%BE%D1%89%D1%8C%D1%8E-js    
    },
    run: async function() {
        await this.getContent()
        this.viewContent()
        let content = document.getElementById('content')
        content.addEventListener('click', this.delContent.bind(this))
    }
}
content.run()

let settings = {
    modalBlock: null,
    globalShadow: null,
    modal: null, // current active modal
    password: false, // does it exist?

    modals: {
        viewModal: function(modalId) { // display the required modal
            const modal = document.getElementById(modalId)
            if (!modal || !settings.modalBlock) return
            settings.modal = modal
            modal.style['display'] = 'block'
            settings.modalBlock.style['display'] = 'block'
        },
        hideModal: function(event) { // hide any modal
            if (
                (event.target != this.globalShadow) &&
                // (event.currentTarget != modalCross) &&
                (event.key != 'Escape')
            ) return
            if (!this.modal || !this.modalBlock) return
            this.modalBlock.style['display'] = 'none'
            this.modal.style['display'] = 'none'
        },
        hideModalCross: function(event) { // hide any modal by cross
            if (event.target.closest('.modal-cross')) {
                if (!this.modalBlock) return
                this.modalBlock.style['display'] = 'none'
                this.modal.style['display'] = 'none'
            }
        },
        openCreateNoteModal: function() { // open modal for creating/editing note
            const modalRecord = document.getElementById('modalRecord')
            if (!modalRecord) return
            
            const whiteMarker = modalRecord.querySelector('input[name="marker"][value="white"]')
            if (whiteMarker) whiteMarker.checked = true
            
            this.modals.viewModal.bind(this)('modalRecord')
        },
        openAddNoteModal: function() { // open modal for adding note
            this.modals.viewModal.bind(this)('modalAddNote')
        },
        openAddImagesModal: function() { // open modal for adding images
            this.modals.viewModal.bind(this)('modalAddImages')
        },
        openEditRecordModal: async function(event) { // open modal for editing record detail
            const modalRecord = document.getElementById('modalRecord')
            if (!modalRecord) return
            
            // Заполняем форму существующими данными из content
            const nameInput = document.getElementById('fNoteName')
            const contentTextarea = document.getElementById('fNoteContent')
            if (nameInput) nameInput.value = content.theme || ''
            if (contentTextarea) contentTextarea.value = content.description || ''
            const colorValue = content.color || 'white'
            const marker = modalRecord.querySelector(`input[name="marker"][value="${colorValue}"]`)
            if (marker) {
                marker.checked = true
            } else {
                const whiteMarker = modalRecord.querySelector('input[name="marker"][value="white"]')
                if (whiteMarker) {
                    whiteMarker.checked = true
                }
            }
            
            this.viewModal('modalRecord')
        },
        openEditImagesModal: async function(event) {  // open modal for editing images group
            // Редактирование группы изображений - открываем модалку для добавления картинок
            const editorPencil = event.target.closest('.images .editor')
            if (editorPencil) {
                event.preventDefault()
                event.stopPropagation()
                const imagesBlock = editorPencil.closest('.images')
                if (imagesBlock && imagesBlock.id) {
                    // Сохраняем msgId в data-атрибуте формы для использования при отправке
                    const form = document.getElementById('addImagesForm')
                    if (form) {
                        form.dataset.editMsgId = imagesBlock.id
                    }
                    // Открываем модалку для добавления картинок (та же, что при создании)
                    this.viewModal('modalAddImages')
                }
            }
        },
        setupFileInputButton: function() { // setup custom file input button
            const fileInput = document.getElementById('fImages')
            const fileInputButton = document.querySelector('.file-input-button')
            if (fileInput && fileInputButton) {
                fileInputButton.addEventListener('click', function(e) {
                    e.preventDefault()
                    fileInput.click()
                })
                
                fileInput.addEventListener('change', function() {
                    if (this.files.length > 0) {
                        const fileCount = this.files.length
                        fileInputButton.textContent = fileCount === 1 ? 'Выбран 1 файл' : `Выбрано ${fileCount} файлов`
                    } else {
                        fileInputButton.textContent = 'Выберите файл'
                    }
                })
            }
        },
        run: function() {
            this.modalBlock = document.getElementById('modalBlock')
            this.globalShadow = document.getElementById('globalShadow')
            
            if (this.modalBlock) {
                this.modalBlock.addEventListener('click', this.modals.hideModal.bind(this))
            }
            document.addEventListener('keyup', this.modals.hideModal.bind(this))
            document.addEventListener('click', this.modals.hideModalCross.bind(this))

            const AddNoteBtn = document.getElementById('AddNoteBtn')
            const AddImagesBtn = document.getElementById('AddImagesBtn')
            AddNoteBtn.addEventListener('click', this.modals.openAddNoteModal.bind(this))
            AddImagesBtn.addEventListener('click', this.modals.openAddImagesModal.bind(this))

            const editorBtn = document.querySelector('.menu-item.editor')  // record update pencil
            if (editorBtn) {
                editorBtn.addEventListener('click', this.modals.openEditRecordModal.bind(this.modals))
            }

            const contentElement = document.getElementById('content')  // images update pencil
            contentElement.addEventListener('click', this.modals.openEditImagesModal.bind(this.modals))

            this.modals.setupFileInputButton.bind(this)()

        }
    },
    
    changeNote: function(event) { // note pencil click
        const editPencil = event.target.closest('.record .edit')
        if (editPencil) {
            const record = editPencil.closest('.record')
            if (record) {
                const recordText = record.querySelector('.record-text')
                if (recordText && !recordText.querySelector('textarea')) {

                    const text = recordText.textContent
                    recordText.innerHTML = ''
                    const textarea = document.createElement('textarea')
                    textarea.value = text
                    textarea.classList.add('record-text-edit')
                    recordText.appendChild(textarea)
                    
                    textarea.style.height = 'auto'
                    textarea.style.height = textarea.scrollHeight + 'px'
                    
                    textarea.focus()
                    // Сохраняем ID заметки в data-атрибуте
                    textarea.dataset.noteId = record.id
                    
                    // Показываем галочку для сохранения
                    const recordHeader = record.querySelector('.record-header')
                    if (recordHeader) {
                        let checkmark = recordHeader.querySelector('.checkmark')
                        const editElement = recordHeader.querySelector('.edit')
                        if (!checkmark) {
                            checkmark = content.createSVG({
                                parent: recordHeader,
                                className: 'checkmark',
                                viewBox: '0 0 507.506 507.506',
                                pathLst: [
                                    'M163.865,436.934c-14.406,0.006-28.222-5.72-38.4-15.915L9.369,304.966c-12.492-12.496-12.492-32.752,0-45.248l0,0   c12.496-12.492,32.752-12.492,45.248,0l109.248,109.248L452.889,79.942c12.496-12.492,32.752-12.492,45.248,0l0,0   c12.492,12.496,12.492,32.752,0,45.248L202.265,421.019C192.087,431.214,178.271,436.94,163.865,436.934z'
                                ],
                            })
                            if (editElement) {
                                recordHeader.insertBefore(checkmark, editElement)
                            }
                        }
                        checkmark.style.display = 'block'
                        if (editElement) {
                            editElement.style.marginLeft = '0'
                        }
                    }
                }
            }
        }
    },

    run: function() {
        this.modals.run.bind(this)()
        
        const contentElement = document.getElementById('content')
        if (contentElement) {
            // Обработчик для карандаша в заметке (note pencil)
            contentElement.addEventListener('click', (event) => {
                this.changeNote(event)
            })
            // Обработчик для галочки в заметке (note checkmark)
            contentElement.addEventListener('click', (event) => {
                const checkmark = event.target.closest('.record .checkmark')
                if (checkmark) {
                    const record = checkmark.closest('.record')
                    if (record && record.id) {
                        content.editNote(Number(record.id))
                    }
                }
            })
        }
    }
}
settings.run()

