import * as conf from "./conf.js";
import { noticeFormUtils } from "./utils/periodic-form-utils.js";
import { slider, sliderView } from "./utils/image-slider.js";
import * as domUtils from "./utils/dom-utils.js";

slider.run()


let queries = {
    noticeId: null, // id of current notice

    createImages: async function(files) { // send creation images form to server
        if (!this.noticeId) {
            console.log('Error: noticeId не установлен')
            return null
        }
        
        const url = conf.Domains['server'] + conf.Urls.noticeImages(this.noticeId)
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
        
        try {
            const response = await fetch(url, options)
            const responseData = await response.json().catch(() => response.text())
            
            if (!response.ok) {
                return { error: true, status: response.status, data: responseData }
            }
            
            return responseData
        } catch (error) {
            return { error: true, message: error.message }
        }
    },
    getImages: async function() { // getting all images from server
        const url = conf.Domains['server'] + conf.Urls.noticeImages(this.noticeId)
        const options = {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
            },
            credentials: 'include',
        }
        const response = await conf.AJAX.send(url, options)
        return response
    },
    delImage: async function(imageId) { // delete any single image
        const url = conf.Domains['server'] + conf.Urls.noticeImage(this.noticeId, imageId)
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
    delImages: async function() { // delete all images for notice
        const url = conf.Domains['server'] + conf.Urls.noticeImages(this.noticeId)
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
    delNotice: async function() { // delete current notice
        const url = conf.Domains['server'] + conf.Urls.FSNotice(this.noticeId)
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
    getNoticeId: function() { // getting notice id from the url
        const pathname = window.location.pathname
        const match = pathname.match(/\/notices\/(\d+)\//)
        if (match && match[1]) {
            return parseInt(match[1], 10)
        }
        console.error('Error: notice ID not found in URL')
        return null
    },
    getContent: async function() { // getting notice data from server
        const url = conf.Domains['server'] + conf.Urls.FSNotice(this.noticeId)
        const options = {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
            },
            credentials: 'include',
        }
        const response = await conf.AJAX.send(url, options)

        if (response === undefined) {
            console.log('Error: неопознанная ошибка при получении напоминания')
            return null
        }

        return response
    },
    updateNotice: async function(data) { // change notice (without images)
        const url = conf.Domains['server'] + conf.Urls.FSNotice(this.noticeId)
        const options = {
            method: 'PATCH',
            headers: {
                'Content-Type': 'application/json',
            },
            credentials: 'include',
            body: JSON.stringify(data || {}),
        }
        const response = await conf.AJAX.send(url, options)
        return response
    },
    run: function() {
        this.noticeId = this.getNoticeId()
    }
}
queries.run()


let content = {
    theme: null,       // title of notice
    description: null, // notice description
    color: null,       // notice color (backend format: w/g/y/r)
    mode: null,        // 'once' | 'periodic'
    raw_data: {        // raw data from server
        date: null,            // backend next_date (YYYY-MM-DD)
        time: null,            // backend time (HH:MM:SS)
        period: null,          // backend period (d,w,m,y format)
    },
    onceData: {        // date info (once mode)
        mode: 'одиночный',     // mode of notice (text)
        date: null,            // date of notice (formatted)
        time: null,            // time of notice (formatted)
    },
    periodicData: {    // date info (periodic mode)
        mode: 'периодический', // mode of notice (text)
        period: null,          // period of notice (user friendly text)
        date: null,            // next date of notice (formatted)
        time: null,            // time of notice (formatted)
    },
    images: [],      // array of images

    getContent: async function() { // parsing data from server
        const data = await queries.getContent()
        if (!data) return

        this.theme = data.title || ''
        this.description = data.description || ''
        this.color = data.color || 'w'
        
        // сохраняем сырые данные от сервера
        this.raw_data.date = data.next_date || ''
        this.raw_data.time = data.time || ''
        this.raw_data.period = data.period || null

        const hasPeriod = !!data.period
        this.mode = hasPeriod ? 'periodic' : 'once'

        const formattedDate = this._formatDate(data.next_date)
        const formattedTime = this._formatTime(data.time)

        if (this.mode === 'once') {
            this.onceData.date = formattedDate
            this.onceData.time = formattedTime
        } else {
            this.periodicData.period = data.period || ''
            this.periodicData.date = formattedDate
            this.periodicData.time = formattedTime
        }

        // Получаем изображения
        const imagesData = await queries.getImages()
        if (imagesData && Array.isArray(imagesData)) {
            this.images = imagesData
        } else {
            this.images = []
        }
    },
    _formatDate: function(dateStr) { // formating date firld
        if (!dateStr) return ''
        const date = new Date(dateStr)
        if (isNaN(date.getTime())) return dateStr
        return date.toLocaleDateString('ru-RU', {
            year: 'numeric',
            month: '2-digit',
            day: '2-digit',
        })
    },
    _formatTime: function(timeStr) { // formating time field
        if (!timeStr) return ''
        // ожидаем формат HH:MM:SS, показываем HH:MM
        return timeStr.slice(0, 5)
    },

    viewContent: function() { // display whole content (with images)
        const themeElement = document.querySelector('.theme')
        themeElement.textContent = this.theme || ''

        const descriptionElement = document.getElementById('description')
        descriptionElement.textContent = this.description || ''

        const onceBlock = document.querySelector('.once-date')
        const periodicBlock = document.querySelector('.periodic-date')

        if (this.mode === 'once') {
            // показываем блок одиночного напоминания, скрываем периодический
            if (onceBlock) onceBlock.style.display = ''
            if (periodicBlock) periodicBlock.style.display = 'none'

            const modeEl = document.getElementById('once-notice-mode')
            const dateEl = document.getElementById('once-notice-date')
            const timeEl = document.getElementById('once-notice-time')

            if (modeEl) modeEl.textContent = this.onceData.mode
            if (dateEl) dateEl.textContent = this.onceData.date || ''
            if (timeEl) timeEl.textContent = this.onceData.time || ''
        } else if (this.mode === 'periodic') {
            // показываем блок периодического напоминания, скрываем одиночный
            if (onceBlock) onceBlock.style.display = 'none'
            if (periodicBlock) periodicBlock.style.display = ''

            const modeEl = document.getElementById('periodic-notice-mode')
            const periodEl = document.getElementById('periodic-notice-period')
            const dateEl = document.getElementById('periodic-notice-date')
            const timeEl = document.getElementById('periodic-notice-time')

            if (modeEl) modeEl.textContent = this.periodicData.mode
            if (periodEl) periodEl.textContent = this.periodicData.period || ''
            if (dateEl) dateEl.textContent = this.periodicData.date || ''
            if (timeEl) timeEl.textContent = this.periodicData.time || ''
        } else {
            // если режим не определён, просто очищаем оба блока
            if (onceBlock) onceBlock.style.display = 'none'
            if (periodicBlock) periodicBlock.style.display = 'none'
        }

        // Отображаем изображения
        this.viewImages()
    },

    editNotice: async function(event) {  // send PATCH and update UI
        event.preventDefault()

        const form = event.target
        const formFields = {
            mode: form.elements['noticeMode'],
            fNoticeName: form.elements['fNoticeName'],
            marker: form.elements['marker'],

            fNoticeDate: form.elements['fNoticeDate'],
            fNoticeTime: form.elements['fNoticeTime'],
            fNoticeDescription: form.elements['fNoticeDescription'],

            fNoticeDay: form.elements['fNoticeDay'],
            fNoticeWeek: form.elements['fNoticeWeek'],
            fNoticeMonth: form.elements['fNoticeMonth'],
            fNoticeYear: form.elements['fNoticeYear'],
            fNoticeInitialDate: form.elements['fNoticeInitialDate'],
            fNoticePeriodTime: form.elements['fNoticePeriodTime'],
            fNoticePeriodDescription: form.elements['fNoticePeriodDescription'],
        }

        const day   = formFields.fNoticeDay.value   || '0'
        const week  = formFields.fNoticeWeek.value  || '0'
        const month = formFields.fNoticeMonth.value || '0'
        const year  = formFields.fNoticeYear.value  || '0'
        const period = `${day},${week},${month},${year}`

        // проверка периодичности
        if (formFields.mode.checked && [day, week, month, year].every(v => v === '0')) {
            const periodErrorField = document.getElementById('periodErrorField')
            if (periodErrorField) {
                periodErrorField.textContent = 'Хотя бы одно поле периодичности должно быть заполнено'
                periodErrorField.style.display = 'block'
            }
            return
        } else {
            const periodErrorField = document.getElementById('periodErrorField')
            if (periodErrorField) {
                periodErrorField.style.display = 'none'
            }
        }

        if (formFields.mode.checked) {
            // проверка длины периода
            if (period.length < 7 || period.length > 9) {
                console.log('Ошибка периода')
                return
            }
            // проверка формата периода
            const re_pattern = /^\d+,\d+,\d+,\d+$/
            if (!re_pattern.test(period)) {
                console.log('Ошибка периода')
                return
            }
        }

        let data
        if (formFields.mode.checked) {  // periodic
            data = {
                title: formFields.fNoticeName.value,
                description: formFields.fNoticePeriodDescription.value.trim() || '',
                color: conf.colors.forward[formFields.marker.value],
                time: formFields.fNoticePeriodTime.value,
                period: period,
                initial_date: formFields.fNoticeInitialDate.value || this.raw_data.date,
            }
        } else {  // once
            data = {
                title: formFields.fNoticeName.value,
                description: formFields.fNoticeDescription.value.trim() || '',
                color: conf.colors.forward[formFields.marker.value],
                time: formFields.fNoticeTime.value,
                initial_date: formFields.fNoticeDate.value || this.raw_data.date,
            }
        }

        // проверка, что initial_date и time еще не прошли
        if (data.initial_date && data.time) {
            const initialDateTime = new Date(`${data.initial_date}T${data.time}`)
            const now = new Date()
            const dateTimeError = document.getElementById('dateTimeError')
            const periodicDateTimeError = document.getElementById('periodicDateTimeError')

            if (initialDateTime <= now) {
                if (formFields.mode.checked) { // period
                    if (periodicDateTimeError) {
                        periodicDateTimeError.textContent = 'Дата и время не могут быть прошедшими'
                        periodicDateTimeError.style.display = 'block'
                    }
                    if (dateTimeError) dateTimeError.style.display = 'none'
                } else {
                    if (dateTimeError) {
                        dateTimeError.textContent = 'Дата и время не могут быть прошедшими'
                        dateTimeError.style.display = 'block'
                    }
                    if (periodicDateTimeError) periodicDateTimeError.style.display = 'none'
                }
                return
            } else {
                if (dateTimeError) dateTimeError.style.display = 'none'
                if (periodicDateTimeError) periodicDateTimeError.style.display = 'none'
            }
        }

        const response = await queries.updateNotice(data)

        if (response === undefined) {
            console.log(`Error: неопознанная ошибка при обновлении напоминания`)
            return
        }

        if (response.success) {
            const resp = response.data

            // обновляем локальное состояние
            this.theme = resp.title
            this.description = resp.description || ''
            this.color = resp.color || 'w'
            
            // обновляем сырые данные от сервера
            this.raw_data.date = resp.next_date || ''
            this.raw_data.time = resp.time || ''
            this.raw_data.period = resp.period || null

            const hasPeriod = !!resp.period
            this.mode = hasPeriod ? 'periodic' : 'once'
            this.periodicData.period = resp.period || null

            const formattedDate = this._formatDate(this.raw_data.date)
            const formattedTime = this._formatTime(this.raw_data.time)

            if (this.mode === 'once') {
                this.onceData.date = formattedDate
                this.onceData.time = formattedTime
            } else {
                this.periodicData.date = formattedDate
                this.periodicData.time = formattedTime
            }

            this.viewContent()

            // сброс полей ошибок
            const periodErrorField = document.getElementById('periodErrorField')
            const dateTimeError = document.getElementById('dateTimeError')
            const periodicDateTimeError = document.getElementById('periodicDateTimeError')
            if (periodErrorField) periodErrorField.textContent = ''
            if (dateTimeError) dateTimeError.style.display = 'none'
            if (periodicDateTimeError) periodicDateTimeError.style.display = 'none'

            // закрываем модалку
            if (settings.modalBlock) settings.modalBlock.style.display = 'none'
            if (settings.modal) settings.modal.style.display = 'none'
        }
    },
    delNotice: async function() { // event of deletion notice by cross
        const response = await queries.delNotice()
        
        if (response === undefined) {
            console.log('Error: неопознанная ошибка при удалении напоминания')
            return
        }
        
        // После успешного удаления перенаправляем на главную страницу
        if (response === 'Напоминание успешно удалено' || response) {
            window.location.href = '/'
        }
    },

    viewImages: function() { // display images slider
        let content = document.getElementById('content')
        if (!content) {
            console.log('Error: не найден контейнер для изображений')
            return
        }
        
        // Очищаем существующий контейнер
        content.innerHTML = ''

        if (this.images && this.images.length > 0) {
            const imagesData = {
                msg_id: queries.noticeId,
                images: this.images
            }
            sliderView.viewImages(imagesData, domUtils)
        }
    },
    handleAddImagesSubmit: async function(event) { // handler for submitting add images form
        event.preventDefault()
        const fileInput = document.getElementById('fImages')
        const files = fileInput.files
        
        if (!files || files.length === 0) {
            console.log('Error: необходимо выбрать хотя бы один файл')
            return
        }
        
        const response = await queries.createImages(files)
        
        if (!response) return
        if (response && typeof response === 'object' && response.error) return
        
        // Успешное сохранение (response - строка или успешный объект)
        if (settings && settings.modalBlock) {
            settings.modalBlock.style.display = 'none'
        }
        
        fileInput.value = ''  // очищаем после отправки формы
        const fileInputButton = document.querySelector('.file-input-button')
        if (fileInputButton) {
            fileInputButton.textContent = 'Выберите файл'
        }
        
        await this.getContent()
        this.viewContent()
    },
    delImage: async function(imageId) { // event of deletion any single image
        const imageIdNum = Number(imageId)
        
        this.images = this.images.filter(img => img.image_id !== imageIdNum)
        
        await queries.delImage(imageIdNum)
        this.viewContent()
    },
    delImages: async function() { // event of deletion all images group
        this.images = []
        await queries.delImages()
        this.viewContent()
    },
    delImagesHandler: function(event) { // event of deletion any type image content by cross
        // cross of any image
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
        
        // cross of the whole images group
        let cross = event.target.closest('.images .cross')
        if (cross) {
            this.delImages()
        }
    },
    updateSliderHeight: function(slider) { // change slider height using the heighter image
        sliderView.updateSliderHeight(slider)
    },
    updateImagesBlockHeight: function() { // пересчет высоты всех блоков изображений на основе самой высокой картинки
        sliderView.updateImagesBlockHeight()
    },
    createElement: function(options) { // create usual HTML elem
        return domUtils.createElement(options)
    },
    createSVG: function(options) { // create usual HTML svg elem
        return domUtils.createSVG(options)
    },
    editTheme: async function() {}, // заготовка
    editDescription: async function() {}, // заготовка
    run: async function() {
        await this.getContent()
        this.viewContent()
        let content = document.getElementById('content')
        if (content) {
            content.addEventListener('click', this.delImagesHandler.bind(this))
        }
        
        const addImagesForm = document.getElementById('addImagesForm')
        if (addImagesForm) {
            addImagesForm.addEventListener('submit', this.handleAddImagesSubmit.bind(this))
        }
    }
}
content.run()


let settings = {
    modalBlock: null,
    globalShadow: null,
    modal: null, // current active modal

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
        openAddImagesModal: function() { // open modal for adding images
            this.viewModal('modalAddImages')
        },
        openEditNoticeModal: async function() { // open modal for editing current notice
            const modalNotice = document.getElementById('modalNotice')
            if (!modalNotice) return

            const form = document.getElementById('crtNoticeForm')
            if (!form) return

            // заголовок и кнопка в режим "Изменение"
            const titleEl = modalNotice.querySelector('.modal-title p')
            const submitBtn = document.getElementById('crtNoticeBtn')
            if (titleEl) titleEl.textContent = 'Изменение напоминания'
            if (submitBtn) submitBtn.textContent = 'Сохранить'

            // заполняем поля существующими данными
            form.fNoticeName.value = content.theme || ''

            const colorValue = conf.colors.revers[content.color] || 'white'
            const marker = modalNotice.querySelector(`input[name="marker"][value="${colorValue}"]`)
            if (marker) {
                marker.checked = true
            } else {
                const whiteMarker = modalNotice.querySelector('input[name="marker"][value="white"]')
                if (whiteMarker) {
                    whiteMarker.checked = true
                }
            }

            const noticeModePeriod = document.getElementById('noticeModePeriod')
            const dateFields = document.getElementById('noticeModeDateFields')
            const periodFields = document.getElementById('noticeModePeriodFields')

            if (content.mode === 'periodic') {
                if (noticeModePeriod) noticeModePeriod.checked = true

                // разбор периода вида "d,w,m,y"
                const raw = content.raw_data.period || ''
                const parts = raw.split(',')
                form.fNoticeDay.value = parts[0] || ''
                form.fNoticeWeek.value = parts[1] || ''
                form.fNoticeMonth.value = parts[2] || ''
                form.fNoticeYear.value = parts[3] || ''

                form.fNoticeInitialDate.value = content.raw_data.date || ''
                form.fNoticePeriodTime.value = content.raw_data.time ? content.raw_data.time.slice(0, 5) : ''
                form.fNoticePeriodDescription.value = content.description || ''
            } else {
                if (noticeModePeriod) noticeModePeriod.checked = false

                form.fNoticeDate.value = content.raw_data.date || ''
                form.fNoticeTime.value = content.raw_data.time ? content.raw_data.time.slice(0, 5) : ''
                form.fNoticeDescription.value = content.description || ''

                // очищаем периодические поля
                form.fNoticeDay.value = ''
                form.fNoticeWeek.value = ''
                form.fNoticeMonth.value = ''
                form.fNoticeYear.value = ''
                form.fNoticeInitialDate.value = ''
                form.fNoticePeriodTime.value = ''
                form.fNoticePeriodDescription.value = ''
            }

            // синхронизируем состояние полей через switchNoticeMode
            if (noticeModePeriod) {
                settings.switchNoticeMode({ target: noticeModePeriod })
            }

            // Заполняем поля "Итоговый период" и "Следующая дата" для периодического режима
            if (content.mode === 'periodic') {
                // Создаем синтетическое событие для вызова функций
                const syntheticEvent = { target: form.fNoticeDay }
                forms.viewPeriodic(syntheticEvent)
                // getNextDate асинхронная, но мы не ждем её завершения
                forms.getNextDate(syntheticEvent)
            }

            this.viewModal('modalNotice')
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

            // Установка значений для импортируемой модалки напоминания на странице notice.html
            const modalNoticeTitle = document.getElementById('modalNoticeTitle')
            const modalNoticeBtn = document.getElementById('crtNoticeBtn')
            if (modalNoticeTitle) modalNoticeTitle.textContent = 'Изменение напоминания'
            if (modalNoticeBtn) modalNoticeBtn.textContent = 'Сохранить'
            
            // switcher periodic mode in the change modal
            const noticeModePeriod = document.getElementById('noticeModePeriod')
            if (noticeModePeriod) {
                noticeModePeriod.addEventListener('change', this.switchNoticeMode.bind(this))
                this.switchNoticeMode({ target: noticeModePeriod })
            }
            
            const AddImagesBtn = document.getElementById('AddImagesBtn')
            AddImagesBtn.addEventListener('click', this.modals.openAddImagesModal.bind(this.modals))

            const editorBtn = document.querySelector('.menu-item.editor')  // record update pencil
            editorBtn.addEventListener('click', this.modals.openEditNoticeModal.bind(this.modals))

            const crossBtn = document.querySelector('.menu-item.cross')  // notice delete cross
            crossBtn.addEventListener('click', content.delNotice.bind(content))

            this.modals.setupFileInputButton.bind(this)()

        }
    },

    switchNoticeMode: function(event) {  // switching period modes for notice form
        const periodModeCheckbox = document.getElementById('noticeModePeriod')
        const dateFields = document.getElementById('noticeModeDateFields')
        const periodFields = document.getElementById('noticeModePeriodFields')
        const modeComment = document.getElementById('noticeModeComment')
        
        // once mode fields
        const fNoticeDate = document.getElementById('fNoticeDate')
        const fNoticeTime = document.getElementById('fNoticeTime')
        
        // periodic mode fields
        const fNoticeDay = document.getElementById('fNoticeDay')
        const fNoticeWeek = document.getElementById('fNoticeWeek')
        const fNoticeMonth = document.getElementById('fNoticeMonth')
        const fNoticeYear = document.getElementById('fNoticeYear')
        const fNoticeInitialDate = document.getElementById('fNoticeInitialDate')
        const fNoticePeriodTime = document.getElementById('fNoticePeriodTime')
        
        if (periodModeCheckbox.checked) {  // period mode
            dateFields.style.display = 'none'
            periodFields.style.display = 'block'
            modeComment.textContent = '(постоянное)'

            if (fNoticeInitialDate) fNoticeInitialDate.required = true
            if (fNoticePeriodTime) fNoticePeriodTime.required = true
            if (fNoticeDate) fNoticeDate.required = false
            if (fNoticeTime) fNoticeTime.required = false
        } else {  // once mode
            dateFields.style.display = 'block'
            periodFields.style.display = 'none'
            modeComment.textContent = '(одиночное)'
            
            if (fNoticeDate) fNoticeDate.required = true
            if (fNoticeTime) fNoticeTime.required = true
            if (fNoticeDay) fNoticeDay.required = false
            if (fNoticeWeek) fNoticeWeek.required = false
            if (fNoticeMonth) fNoticeMonth.required = false
            if (fNoticeYear) fNoticeYear.required = false
            if (fNoticeInitialDate) fNoticeInitialDate.required = false
            if (fNoticePeriodTime) fNoticePeriodTime.required = false
        }
    },

    run: function() {
        this.modals.run.bind(this)()

        const crtNoticeForm = document.getElementById('crtNoticeForm')
        crtNoticeForm.addEventListener('submit', content.editNotice.bind(content))
        
    }
}
settings.run()

let forms = {
    viewPeriodic: function(event) {  // display user friendly periodic script in the form
        noticeFormUtils.viewPeriodic(event)  // implementation in the utils folder
    },
    getNextDate: async function(event) {  // display next date using period in the form
        await noticeFormUtils.getNextDate(event)  // implementation in the utils folder
    },
    run: function() {
        // view periodicity
        const fNoticeDay = document.getElementById('fNoticeDay')
        const fNoticeWeek = document.getElementById('fNoticeWeek')
        const fNoticeMonth = document.getElementById('fNoticeMonth')
        const fNoticeYear = document.getElementById('fNoticeYear')
        fNoticeDay.addEventListener('change', this.viewPeriodic.bind(this))
        fNoticeWeek.addEventListener('change', this.viewPeriodic.bind(this))
        fNoticeMonth.addEventListener('change', this.viewPeriodic.bind(this))
        fNoticeYear.addEventListener('change', this.viewPeriodic.bind(this))

        const fNoticeInitialDate = document.getElementById('fNoticeInitialDate')
        const fNoticePeriodTime = document.getElementById('fNoticePeriodTime')
        fNoticeDay.addEventListener('change', this.getNextDate.bind(this))
        fNoticeWeek.addEventListener('change', this.getNextDate.bind(this))
        fNoticeMonth.addEventListener('change', this.getNextDate.bind(this))
        fNoticeYear.addEventListener('change', this.getNextDate.bind(this))
        fNoticeInitialDate.addEventListener('change', this.getNextDate.bind(this))
        fNoticePeriodTime.addEventListener('change', this.getNextDate.bind(this))
    }
}
forms.run()
