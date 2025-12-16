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
    updateNote: function(noteId) { // change any comment

    },
    updateRecord: function() { // change record (settings and theme)

    },
    delNote: function(noteId) { // delete any note

    },
    delImages: function(imagesId) { // delete any images group

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
        
        const response = await this.createImages(files)
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
        }
    },
    run: function() {
        this.recordId = this.getRecordId()
        
        const addNoteForm = document.getElementById('addNoteForm')
        const addImagesForm = document.getElementById('addImagesForm')
        addNoteForm.addEventListener('submit', this.handleAddNoteSubmit.bind(this))
        addImagesForm.addEventListener('submit', this.handleAddImagesSubmit.bind(this))
    }
}
queries.run()

let content = {
    theme: null, // title of whole record
    description: null, // record rescription
    messages: {},

    getContent: async function() { // parsing data (details and messages) from server
        const {messages: messages, record: recordDetail} = await queries.getContent()
        // recordDetail - {record_id: 19, user_id: 1, title: 'record 1'} позже добавится description
        this.theme = recordDetail.title
        this.messages = messages
    },
    viewContent: function() { // display messages by msg type
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
    delContent: function(event) { // event of deletion any type content by cross
        // image cross
        let imageCross = event.target.closest('.image-cross')
        if (imageCross) {
            let image = imageCross.closest('.image')
            if (image) {
                let img = image.querySelector('img')
                if (img && img.id) {
                    this.delImage(Number(img.id))
                    return
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
    delNote: function(recordId) { // event of deletion any note
        delete this.notes[Number(recordId)]
        for (let i=0; i < this.content.length; i++) {
            if (!this.content[i].type === 'note') continue
            if (this.content[i].id === Number(recordId)) {
                this.content.splice(i, 1)
            }
        }
        // ajax delete note
        this.viewContent()
    },
    delImage: function(imageId) { // event of deletion any single image
        // Удаляем объект Image
        delete this.images[Number(imageId)]
        
        // Находим группу изображений, содержащую эту картинку
        let groupId = null
        for (let groupKey in this.imagesGroups) {
            let contentArray = this.imagesGroups[groupKey].content
            let imageIndex = contentArray.indexOf(Number(imageId))
            if (imageIndex !== -1) {
                groupId = Number(groupKey)
                // Удаляем ID картинки из массива content группы
                contentArray.splice(imageIndex, 1)
                
                // Если группа стала пустой, удаляем всю группу
                if (contentArray.length === 0) {
                    delete this.imagesGroups[groupId]
                    // Удаляем группу из content массива
                    for (let i=0; i < this.content.length; i++) {
                        if (this.content[i].type === 'imagesGroup' && this.content[i].id === groupId) {
                            this.content.splice(i, 1)
                            break
                        }
                    }
                }
                break
            }
        }
        
        // ajax delete image
        this.viewContent()
        // Пересчитываем высоту только того блока, из которого была удалена картинка
        // Используем небольшую задержку, чтобы дать время изображениям загрузиться
        if (groupId !== null) {
            setTimeout(() => {
                let imagesBlock = document.getElementById(String(groupId))
                if (imagesBlock) {
                    let slider = imagesBlock.querySelector('.slider')
                    if (slider) {
                        this.updateSliderHeight(slider)
                    }
                }
            }, 100)
        }
    },
    updateSliderHeight: function(slider) { // пересчет высоты конкретного блока slider на основе самой высокой картинки
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
        
        // Устанавливаем высоту блока на основе самой высокой картинки
        // Ограничиваем максимальной высотой 300px из CSS
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
    delImages: function(imagesId) { // event of deletion any image group (with images)
        for (let i=0; i<this.imagesGroups[Number(imagesId)].content.length; i++) {
            let num = this.imagesGroups[Number(imagesId)].content[i]
            delete this.images[num]
        }
        // ajax delete images
        delete this.imagesGroups[Number(imagesId)]
        for (let i=0; i < this.content.length; i++) {
            if (!this.content[i].type === 'imagesGroup') continue
            if (this.content[i].id === Number(imagesId)) {
                this.content.splice(i, 1)
            }
        }
        // ajax delete imagesGroups
        this.viewContent()
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
        // Заглушка для даты (в будущем будет приходить из noteData.date)
        let currentDate = new Date()
        let dateString = currentDate.toLocaleDateString('ru-RU', {
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
            this.modal = document.getElementById(modalId)
            if (!this.modal || !this.modalBlock) return
            this.modal.style['display'] = 'block'
            this.modalBlock.style['display'] = 'block'
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

            // Add click handler for editor button
            const editorBtn = document.querySelector('.menu-item.editor')
            if (editorBtn) {
                editorBtn.addEventListener('click', this.modals.openCreateNoteModal.bind(this))
            }

            const AddNoteBtn = document.getElementById('AddNoteBtn')
            const AddImagesBtn = document.getElementById('AddImagesBtn')
            AddNoteBtn.addEventListener('click', this.modals.openAddNoteModal.bind(this))
            AddImagesBtn.addEventListener('click', this.modals.openAddImagesModal.bind(this))

            this.modals.setupFileInputButton.bind(this)()

        }
    },
    otherSite: {
        delRecord: function(event) { // btn of whole record deletion
            // ajax del whole record
            window.location.pathname = '/notes'
        },
        hideModalBtn: function() { // hide any modal by inner btn click
            if (!this.modal || !this.modalBlock) return
            this.modalBlock.style['display'] = 'none'
            this.modal.style['display'] = 'none'
        },
        run: function() {

        }
    },
    run: function() {
        this.modals.run.bind(this)()
        this.otherSite.run.bind(this)()
    }
}
settings.run()

