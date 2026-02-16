import * as conf from "./conf.js";
import { noticeFormUtils } from "./utils/periodic-form-utils.js";

let session = {
    section: sessionStorage.getItem('section')?
             sessionStorage.getItem('section'):
             'notes',
}
session.section

const DADSettings = {  // general settings for DAD
    "DADObjectHeight": '58px',  // минимальный размер папок и записей
    "putBeetwenArea": 14.5,  // высота области (px) для логики "перемещения между" (в противовес перемещению внутрь)
    "draggableClass": 'draggableObject',  // название класса, который участвует в DAD
    "folderClass": 'folder',  // название класса у каждой папки
    "recordClass": 'record',  // название класса у каждой записи
}
const stickyDADSettings = {  // size of DAD Object
    "width": 300,
    "height": 44,
    "opacity": '60%',
    "border-color": 'rgb(255, 0, 221)',
}
const classNames = {
    settingIcon: 'setting-field',  // gear for each records and folders
    backFolder: 'folder-back',  // folder for moving back in the directory
    stickyDAD: 'stickyDAD'  // an object attached to the mouse
}

let modals = {
    modal: null,     // link to the currently open modal (DOM-element)
    mode: 'create',  // 'create' или 'edit'
    editId: null,    // ID редактируемого объекта
    editType: null,  // 'record' или 'folder'

    sort: { // blank

        byAlphabet: function() {
            console.log('сортировка по алфавиту')
        },
        byDate: function() {
            console.log('сортировка по дате')
        },
        Custom: function() {
            console.log('пользовательская сортировка')
        },
    },
    hideModal: function(event) {  // modal closing
        if (
            (event.target != globalShadow) &&  // outside click
            // (event.currentTarget != modalCross) &&  // hideModalCross func
            (event.key != 'Escape')  // esc click
        ) return
        if (!this.modal) return
        modalBlock.style['display'] = 'none'
        console.log('this.modal', this.modal)
        this.modal.style['display'] = 'none'
        this.resetMode()
    },
    hideModalCross: function(event) {  // modal closing
        if (event.target.closest('.modal-cross')) {  // cross click
            modalBlock.style['display'] = 'none'
            this.modal.style['display'] = 'none'
            this.resetMode()
        }
    },
    resetMode: function() {  // reset modal settings for create and edit forms
        // Сброс режима и UI при закрытии модалки
        this.mode = 'create'
        this.editId = null
        this.editType = null
        
        // Сброс заголовков и кнопок
        const modalRecord = document.getElementById('modalRecord')
        const modalFolder = document.getElementById('modalFolder')
        const modalNotice = document.getElementById('modalNotice')
        
        if (modalRecord) {
            modalRecord.querySelector('.modal-title p').textContent = 'Создание заметки'
            modalRecord.querySelector('button[type="submit"]').textContent = 'Создать'
            document.getElementById('crtRecordForm').reset()
        }
        if (modalFolder) {
            modalFolder.querySelector('.modal-title p').textContent = 'Создание папки'
            modalFolder.querySelector('button[type="submit"]').textContent = 'Создать'
            document.getElementById('crtFolderForm').reset()
        }
        if (modalNotice) {
            modalNotice.querySelector('.modal-title p').textContent = 'Создание напоминания'
            modalNotice.querySelector('button[type="submit"]').textContent = 'Создать'
            document.getElementById('crtNoticeForm').reset()
            
            // Сброс режима формы в состояние "одиночное" (unchecked)
            const noticeModePeriod = document.getElementById('noticeModePeriod')
            noticeModePeriod.checked = false
            forms.switchNoticeMode({ target: noticeModePeriod })
        }
    },
    getModal: function(event) {  // select modal for 3 btn of creation and sort
        // сейчас функция не учитывает, что может быть сортировка (исправить-удалить)
        this.modal = document.getElementById(event.target.dataset.modal)
        this.modal.style['display'] = 'block'
        modalBlock.style['display'] = 'block'
        
        // the creation mode on
        this.mode = 'create'
        this.editId = null
        this.editType = null
        
        if (this.modal.id === 'modalNotice') {  // creation notice form
            forms.setInitialDate()
        }
    },
    openEditModal: function(type, id) {  // openning modal using edit mode 
        this.mode = 'edit'
        this.editId = parseInt(id)
        this.editType = type
        
        let modalId, form, titleText, data  // defining current form data
        
        if (type === 'record') {
            modalId = 'modalRecord'
            form = document.getElementById('crtRecordForm')
            titleText = 'Редактирование заметки'
            data = content.notes[id]

            form.fNoteName.value = data.title
            form.fNoteContent.value = data.description || ''
            const colorValue = conf.colors.revers[data.color] || 'white'
            const markerRadio = form.querySelector(`input[name="marker"][value="${colorValue}"]`)
            if (markerRadio) markerRadio.checked = true
            
        } else if (type === 'folder') {
            modalId = 'modalFolder'
            form = document.getElementById('crtFolderForm')
            titleText = 'Редактирование папки'
            data = content.noteFolders[id].info

            form.fFolderName.value = data.title
            const colorValue = conf.colors.revers[data.color] || 'white'
            const markerRadio = form.querySelector(`input[name="marker"][value="${colorValue}"]`)
            if (markerRadio) markerRadio.checked = true
        }
        
        // fill the form using current data
        this.modal = document.getElementById(modalId)
        this.modal.querySelector('.modal-title p').textContent = titleText
        this.modal.querySelector('button[type="submit"]').textContent = 'Сохранить'

        this.modal.style.display = 'block'
        modalBlock.style.display = 'block'
    },
    openEditNoticeModal: function(type, id) {  // opening modal using edit mode for notices
        this.mode = 'edit'
        this.editId = parseInt(id)
        this.editType = type
        
        let modalId, form, titleText, data  // defining current form data
        
        if (type === 'record') {
            modalId = 'modalNotice'
            form = document.getElementById('crtNoticeForm')
            titleText = 'Редактирование напоминания'
            data = content.notices[id]

            form.fNoticeName.value = data.title
            const colorValue = conf.colors.revers[data.color] || 'white'
            const markerRadio = form.querySelector(`input[name="marker"][value="${colorValue}"]`)
            if (markerRadio) markerRadio.checked = true
            
            if (data.period) { //periodic
                const noticeModePeriod = document.getElementById('noticeModePeriod')
                form.noticeMode.checked = true
                forms.switchNoticeMode({ target: noticeModePeriod })

                form.fNoticeDay.value = data.period.split(',')[0]
                form.fNoticeWeek.value = data.period.split(',')[1]
                form.fNoticeMonth.value = data.period.split(',')[2]
                form.fNoticeYear.value = data.period.split(',')[3]
                form.fNoticeInitialDate.value = data.date
                form.fNoticePeriodTime.value = data.time
                form.fNoticePeriodDescription.value = data.description
                
                // Заполняем поля "Итоговый период" и "Следующая дата"
                const syntheticEvent = { target: form.fNoticeDay }
                forms.viewPeriodic(syntheticEvent)
                forms.getNextDate(syntheticEvent)
                
            } else { // once
                form.fNoticeDate.value = data.date
                form.fNoticeTime.value = data.time
                form.fNoticeDescription.value = data.description
            }
        } else if (type === 'folder') {
            modalId = 'modalFolder'
            form = document.getElementById('crtFolderForm')
            titleText = 'Редактирование папки'
            data = content.noticeFolders[id].info

            form.fFolderName.value = data.title
            const colorValue = conf.colors.revers[data.color] || 'white'
            const markerRadio = form.querySelector(`input[name="marker"][value="${colorValue}"]`)
            if (markerRadio) markerRadio.checked = true
        }
        
        this.modal = document.getElementById(modalId)
        this.modal.querySelector('.modal-title p').textContent = titleText
        this.modal.querySelector('button[type="submit"]').textContent = 'Сохранить'

        this.modal.style.display = 'block'
        modalBlock.style.display = 'block'
    },
    run: function() {
        modalBlock.addEventListener('click', this.hideModal.bind(this))
        document.addEventListener('click', this.hideModalCross.bind(this))

        modalSortBtn.addEventListener('click', this.getModal.bind(this))
        modalCreateBtn.addEventListener('click', this.getModal.bind(this))
        modalCreateFBtn.addEventListener('click', this.getModal.bind(this))

        document.addEventListener('keyup', this.hideModal.bind(this))

        // Установка значений для модалок на главной странице
        const modalRecordTitle = document.getElementById('modalRecordTitle')
        const modalRecordBtn = document.getElementById('crtRecordBtn')
        if (modalRecordTitle) modalRecordTitle.textContent = 'Создание заметки'
        if (modalRecordBtn) modalRecordBtn.textContent = 'Создать'

        const modalNoticeTitle = document.getElementById('modalNoticeTitle')
        const modalNoticeBtn = document.getElementById('crtNoticeBtn')
        if (modalNoticeTitle) modalNoticeTitle.textContent = 'Создание напоминания'
        if (modalNoticeBtn) modalNoticeBtn.textContent = 'Создать'
    }
}
modals.run()

const forms = {
    handleRecordSubmit: async function(event) {  // select form action by mode (create / update) for records
        event.preventDefault()
        
        if (modals.mode === 'edit') {
            await this.updateRecord(event)
        } else {
            await this.createRecord(event)
        }
        modals.resetMode()
    },
    createRecord: async function(event) {  // creation a new record (ajax and ui)
        const form = event.target
        const data = {
            folder_id: parseInt(viewContent.currentFolderId),
            title: form.fNoteName.value,
            description: form.fNoteContent.value.trim() || '',
            color: conf.colors.forward[form.marker.value],
        }

        const url = conf.Domains['server'] + conf.Urls.FSRecords
        const options = {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            credentials: 'include',
            body: JSON.stringify(data),
        }
        const response = await conf.AJAX.send(url, options)

        if (response === undefined) {
            console.log(`Error: неопознанная ошибка`)
            return
        }
        
        if (response.success) {
            const resp_data = {
                pk: parseInt(response.data['pk']),
                title: response.data['title'],
                folder_id: parseInt(response.data['folder_id']),
                color: conf.colors.revers[response.data['color']],
                changed_at: response.data['changed_at'],
                description: response.data['description'] || ''
            }
            content.change.addNote(resp_data)

            modalBlock.style['display'] = 'none'
            modals.modal.style['display'] = 'none'
        }
    },
    updateRecord: async function(event) {  // updating the record (ajax and ui)
        const form = event.target
        const id = modals.editId
        const data = {
            title: form.fNoteName.value,
            description: form.fNoteContent.value.trim() || '',
            color: conf.colors.forward[form.marker.value],
        }
        console.log('Обновление записи:', id, data)

        const url = conf.Domains['server'] + conf.Urls.FSRecord(id)
        const options = {
            method: 'PATCH',
            headers: {
                'Content-Type': 'application/json',
            },
            credentials: 'include',
            body: JSON.stringify(data),
        }
        const response = await conf.AJAX.send(url, options)

        if (response === undefined) {
            console.log(`Error: неопознанная ошибка`)
            return
        }
        
        if (response.success) {
            content.notes[id].title = response.data['title']
            content.notes[id].description = response.data['description'] || ''
            content.notes[id].color = response.data['color']  // цвет уже в коротком формате ('w', 'g', 'y', 'r')
            content.notes[id].changed_at = response.data['changed_at']
            
            viewContent.removeObjects()
            viewContent.displayItems()
            
            modalBlock.style['display'] = 'none'
            modals.modal.style['display'] = 'none'
            modals.resetMode()
        }
    },

    handleFolderSubmit: async function(event) {  // select form action by mode (create / update) for folders
        event.preventDefault()
        if (modals.mode === 'edit') {
            if (session.section == 'notes') {
                await this.updateRecordFolder(event)
            } else {
                await this.updateNoticeFolder(event)
            }
        } else {
            if (session.section == 'notes') {
                await this.createRecordFolder(event)
            } else {
                await this.createNoticeFolder(event)
            }
        }
        modals.resetMode()
    },
    createRecordFolder: async function(event) {  // creation a new record folder (ajax and ui)
        const form = event.target
        const data = {
            parent_id: parseInt(viewContent.currentFolderId),
            title: form.fFolderName.value,
            color: conf.colors.forward[form.marker.value],
        }
        console.log(data)

        const url = conf.Domains['server'] + conf.Urls.FSFolders
        const options = {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            credentials: 'include',
            body: JSON.stringify(data),
        }
        const response = await conf.AJAX.send(url, options)

        if (response === undefined) {
            console.log(`Error: неопознанная ошибка`)
            return
        }
        
        if (response.success) {
            const resp_data = {
                pk: parseInt(response.data['pk']),
                parent_id: parseInt(response.data['parent_id']),
                title: response.data['title'],
                color: conf.colors.revers[response.data['color']],
                changed_at: response.data['changed_at'],
                children: response.data['children'] || ''
            }
            content.change.addNoteFolder(resp_data)

            modalBlock.style['display'] = 'none'
            modals.modal.style['display'] = 'none'
        }
        
    },
    updateRecordFolder: async function(event) {  // updating the record folder (ajax and ui)
        const form = event.target
        const id = modals.editId
        const data = {
            title: form.fFolderName.value,
            color: conf.colors.forward[form.marker.value],
        }
        console.log('Обновление папки:', id, data)

        const url = conf.Domains['server'] + conf.Urls.FSFolder(id)
        const options = {
            method: 'PATCH',
            headers: {
                'Content-Type': 'application/json',
            },
            credentials: 'include',
            body: JSON.stringify(data),
        }
        const response = await conf.AJAX.send(url, options)

        if (response === undefined) {
            console.log(`Error: неопознанная ошибка`)
            return
        }
        
        if (response.success) {
            content.noteFolders[id].info.title = response.data['title']
            content.noteFolders[id].info.color = response.data['color']
            content.noteFolders[id].info.changed_at = response.data['changed_at']
            
            viewContent.removeObjects()
            viewContent.displayItems()
            
            modalBlock.style['display'] = 'none'
            modals.modal.style['display'] = 'none'
            modals.resetMode()
        }
    },

    handleNoticeSubmit: async function(event) {  // select form action by mode (create / update) for folders
        event.preventDefault()
        if (modals.mode === 'edit') {
            await this.updateNotice(event)
        } else {
            await this.createNotice(event)
        }
        modals.resetMode()
    },
    createNotice: async function(event) {  // blank for creation a notice
        event.preventDefault()
        console.log('createNotice')

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

        if (formFields.mode.checked && [day, week, month, year].every(v => v==='0')) {
            const periodErrorField = document.getElementById('periodErrorField')
            periodErrorField.textContent = 'Хотя бы одно поле периодичности должно быть заполнено'
            periodErrorField.style.display = 'block'
            return
        } else {
            const periodErrorField = document.getElementById('periodErrorField')
            periodErrorField.style.display = 'none'
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
                folder_id: parseInt(viewContent.currentFolderId),
                title: formFields.fNoticeName.value,
                description: formFields.fNoticePeriodDescription.value.trim() || '',
                color: conf.colors.forward[formFields.marker.value],
                time: formFields.fNoticePeriodTime.value,
                period: period,
                initial_date: formFields.fNoticeInitialDate.value,
            }
        } else {  // once
            data = {
                folder_id: parseInt(viewContent.currentFolderId),
                title: formFields.fNoticeName.value,
                description: formFields.fNoticeDescription.value.trim() || '',
                color: conf.colors.forward[formFields.marker.value],
                time: formFields.fNoticeTime.value,
                // period: '',
                initial_date: formFields.fNoticeDate.value,
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
                    periodicDateTimeError.textContent = 'Дата и время не могут быть прошедшими'
                    periodicDateTimeError.style.display = 'block'
                    if (dateTimeError) dateTimeError.style.display = 'none'
                } else {
                    dateTimeError.textContent = 'Дата и время не могут быть прошедшими'
                    dateTimeError.style.display = 'block'
                    if (periodicDateTimeError) periodicDateTimeError.style.display = 'none'
                }
                return
            } else {
                if (dateTimeError) dateTimeError.style.display = 'none'
                if (periodicDateTimeError) periodicDateTimeError.style.display = 'none'
            }
        }

        const url = conf.Domains['server'] + conf.Urls.FSNotices
        const options = {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            credentials: 'include',
            body: JSON.stringify(data),
        }
        
        const response = await conf.AJAX.send(url, options)

        if (response === undefined) {
            console.log(`Error: неопознанная ошибка`)
            return
        }
        
        if (response.success) {
            const resp_data = {
                pk: parseInt(response.data['pk']),
                title: response.data['title'],
                folder_id: parseInt(response.data['folder_id']),
                color: conf.colors.revers[response.data['color']],
                changed_at: response.data['changed_at'],
                description: response.data['description'] || '',
                next_date: response.data['next_date'] || '',
                time: response.data['time'] || '',
                period: response.data['period'] || '',
            }
            content.change.addNotice(resp_data)

            // сброс формы и полей ошибок
            form.reset()
            const noticeModePeriod = document.getElementById('noticeModePeriod')
            if (noticeModePeriod) {
                noticeModePeriod.checked = false
                forms.switchNoticeMode({ target: noticeModePeriod })
            }
            const periodErrorField = document.getElementById('periodErrorField')
            const dateTimeError = document.getElementById('dateTimeError')
            const periodicDateTimeError = document.getElementById('periodicDateTimeError')
            if (periodErrorField) periodErrorField.textContent = ''
            if (dateTimeError) dateTimeError.style.display = 'none'
            if (periodicDateTimeError) periodicDateTimeError.style.display = 'none'

            modalBlock.style['display'] = 'none'
            modals.modal.style['display'] = 'none'
        }
    },
    updateNotice: async function(event) {  // updating the notice (ajax and ui)
        event.preventDefault()
        console.log('updateNotice')

        const form = event.target
        const id = modals.editId
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

        if (formFields.mode.checked && [day, week, month, year].every(v => v==='0')) {
            const periodErrorField = document.getElementById('periodErrorField')
            periodErrorField.textContent = 'Хотя бы одно поле периодичности должно быть заполнено'
            periodErrorField.style.display = 'block'
            return
        } else {
            const periodErrorField = document.getElementById('periodErrorField')
            periodErrorField.style.display = 'none'
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
                initial_date: formFields.fNoticeInitialDate.value,
            }
        } else {  // once
            data = {
                title: formFields.fNoticeName.value,
                description: formFields.fNoticeDescription.value.trim() || '',
                color: conf.colors.forward[formFields.marker.value],
                time: formFields.fNoticeTime.value,
                initial_date: formFields.fNoticeDate.value,
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
                    periodicDateTimeError.textContent = 'Дата и время не могут быть прошедшими'
                    periodicDateTimeError.style.display = 'block'
                    if (dateTimeError) dateTimeError.style.display = 'none'
                } else {
                    dateTimeError.textContent = 'Дата и время не могут быть прошедшими'
                    dateTimeError.style.display = 'block'
                    if (periodicDateTimeError) periodicDateTimeError.style.display = 'none'
                }
                return
            } else {
                if (dateTimeError) dateTimeError.style.display = 'none'
                if (periodicDateTimeError) periodicDateTimeError.style.display = 'none'
            }
        }

        const url = conf.Domains['server'] + conf.Urls.FSNotice(id)
        const options = {
            method: 'PATCH',
            headers: {
                'Content-Type': 'application/json',
            },
            credentials: 'include',
            body: JSON.stringify(data),
        }
        
        const response = await conf.AJAX.send(url, options)

        if (response === undefined) {
            console.log(`Error: неопознанная ошибка`)
            return
        }
        
        if (response.success) {
            // обновление объекта notice в content
            content.notices[id].title = response.data['title']
            content.notices[id].description = response.data['description'] || ''
            content.notices[id].color = conf.colors.revers[response.data['color']] || content.notices[id].color
            content.notices[id].changed_at = response.data['changed_at']
            content.notices[id].date = response.data['next_date'] || ''
            content.notices[id].time = response.data['time'] || ''
            content.notices[id].period = response.data['period'] || ''
            
            viewContent.removeObjects()
            viewContent.displayItems()
            
            // сброс полей ошибок
            const periodErrorField = document.getElementById('periodErrorField')
            const dateTimeError = document.getElementById('dateTimeError')
            const periodicDateTimeError = document.getElementById('periodicDateTimeError')
            if (periodErrorField) periodErrorField.textContent = ''
            if (dateTimeError) dateTimeError.style.display = 'none'
            if (periodicDateTimeError) periodicDateTimeError.style.display = 'none'

            modalBlock.style['display'] = 'none'
            modals.modal.style['display'] = 'none'
            modals.resetMode()
        }
    },

    createNoticeFolder: async function(event) {  // blank for creation a new notice folder
        event.preventDefault()
        console.log('createNoticeFolder')

        const form = event.target
        const data = {
            parent_id: parseInt(viewContent.currentFolderId),
            title: form.fFolderName.value,
            color: conf.colors.forward[form.marker.value],
        }
        console.log(data)

        const url = conf.Domains['server'] + conf.Urls.FSFoldersNotice
        const options = {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            credentials: 'include',
            body: JSON.stringify(data),
        }
        const response = await conf.AJAX.send(url, options)

        if (response === undefined) {
            console.log(`Error: неопознанная ошибка`)
            return
        }
        
        if (response.success) {
            const resp_data = {
                pk: parseInt(response.data['pk']),
                parent_id: parseInt(response.data['parent_id']),
                title: response.data['title'],
                color: conf.colors.revers[response.data['color']],
                changed_at: response.data['changed_at'],
                children: response.data['children'] || ''
            }
            content.change.addNoticeFolder(resp_data)

            modalBlock.style['display'] = 'none'
            modals.modal.style['display'] = 'none'
        }

    },
    updateNoticeFolder: async function(event) {  // updating the notice folder (ajax and ui)
        const form = event.target
        const id = modals.editId
        const data = {
            title: form.fFolderName.value,
            color: conf.colors.forward[form.marker.value],
        }
        console.log('Обновление папки напоминаний:', id, data)

        const url = conf.Domains['server'] + conf.Urls.FSFolderNotice(id)
        const options = {
            method: 'PATCH',
            headers: {
                'Content-Type': 'application/json',
            },
            credentials: 'include',
            body: JSON.stringify(data),
        }
        const response = await conf.AJAX.send(url, options)

        if (response === undefined) {
            console.log(`Error: неопознанная ошибка`)
            return
        }
        
        if (response.success) {
            content.noticeFolders[id].info.title = response.data['title']
            content.noticeFolders[id].info.color = response.data['color']
            content.noticeFolders[id].info.changed_at = response.data['changed_at']
            
            viewContent.removeObjects()
            viewContent.displayItems()
            
            modalBlock.style['display'] = 'none'
            modals.modal.style['display'] = 'none'
            modals.resetMode()
        }
    },
    setInitialDate: function() {  // set today in the date field
        const initialDateInput = document.getElementById('fNoticeInitialDate')
        if (initialDateInput) {
            const today = new Date()
            const year = today.getFullYear()
            const month = String(today.getMonth() + 1).padStart(2, '0')
            const day = String(today.getDate()).padStart(2, '0')
            initialDateInput.value = `${year}-${month}-${day}`
        }
    },
    
    switchNoticeMode: function(event) {  // switching between date and period modes for notice form
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
            if (modeComment) {
                modeComment.textContent = '(постоянное)'
            }

            if (fNoticeInitialDate) fNoticeInitialDate.required = true
            if (fNoticePeriodTime) fNoticePeriodTime.required = true
            if (fNoticeDate) fNoticeDate.required = false
            if (fNoticeTime) fNoticeTime.required = false
        } else {  // once mode
            dateFields.style.display = 'block'
            periodFields.style.display = 'none'
            if (modeComment) {
                modeComment.textContent = '(одиночное)'
            }
            
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
    viewPeriodic: function(event) {  // display user friendly periodic script in the form
        noticeFormUtils.viewPeriodic(event)  // implementation in the utils folder
    },
    getNextDate: async function(event) {  // display next date using period in the form
        await noticeFormUtils.getNextDate(event)  // implementation in the utils folder
    },
    run: function() {
        const crtRecordForm = document.getElementById('crtRecordForm')
        const crtNoticeForm = document.getElementById('crtNoticeForm')
        const crtFolderForm = document.getElementById('crtFolderForm')
        
        crtRecordForm.addEventListener('submit', this.handleRecordSubmit.bind(this))
        crtNoticeForm.addEventListener('submit', this.handleNoticeSubmit.bind(this))
        crtFolderForm.addEventListener('submit', this.handleFolderSubmit.bind(this))
        
        // notice form mode switcher
        const noticeModePeriod = document.getElementById('noticeModePeriod')
        if (noticeModePeriod) {
            noticeModePeriod.addEventListener('change', this.switchNoticeMode.bind(this))
            this.switchNoticeMode({ target: noticeModePeriod })
        }

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

let search = {
    getSearchList: function() {  // getting a search list
        const searchListTest = [ // Заглушка для теста до получения настоящего контента
            'О Нас',
            'Основа',
            'Блог',
            'Контакт',
            'Заказ',
            'Поддержка',
            'Инструменты',
        ]
        return searchListTest
    },
    showSearchList: function(event) {  // display the drop down list
        if (event.target != searchQueryInput) return // событие вне search поля (доп. проверка)

        let searchValueUpper = searchQueryInput.value.toUpperCase()
        if (searchValueUpper == '') { // если поисковое слово удалено
            searchDropdown.style['display'] = 'none'
            searchDropdown.innerHTML = ''
            return
        }

        searchDropdown.style['display'] = 'block'
        searchDropdown.innerHTML = ''
        const searchListOriginal = this.getSearchList()
        let seacrhListFiltered = []
        for (let i = 0; i < searchListOriginal.length; i++) {
            if (searchListOriginal[i].toUpperCase().includes(searchValueUpper)) {
                seacrhListFiltered.push(searchListOriginal[i])
            }
        }
        for (let i = 0; i < seacrhListFiltered.length; i++) {
            const searchElemI = document.createElement('a')
            searchElemI.href = '#' + seacrhListFiltered[i]
            searchElemI.innerHTML = seacrhListFiltered[i]
            searchDropdown.append(searchElemI)
        }
    },
    hideSearchList: function(event) {  // deletion the drop down list
        if (searchDropdown.style['display'] != 'block') return // выпадающего списка нет
        if (event.target == searchQueryInput) return // нажатие по поисковой строке
        searchDropdown.style['display'] = 'none'
        searchDropdown.innerHTML = ''
    },
    run: function() {
        searchQueryInput.addEventListener('input', this.showSearchList.bind(this))
        document.addEventListener('click', this.hideSearchList.bind(this))
    }
}
search.run()

let Header = {
    updateCreateButtonsDataset: function() {  // обновление dataset кнопок создания в зависимости от секции
        const modalCreateBtn = document.getElementById('modalCreateBtn')
        const modalCreateFBtn = document.getElementById('modalCreateFBtn')
        
        const mode = session.section === 'notes' ? 'modalRecord' : 'modalNotice'
        modalCreateBtn.dataset.modal = mode
        modalCreateFBtn.dataset.modal = 'modalFolder'
    },
    handleSectionChange: function(event) {  // custom header event of change section
        const section = event.detail.section
        session.section = section

        if (session.section === 'notes') {
            viewContent.currentFolderId = content.notesRoot
        } else if (session.section === 'notices') {
            viewContent.currentFolderId = content.noticesRoot
        }
        
        this.updateCreateButtonsDataset()
        
        viewContent.removeObjects()
        viewContent.displayItems()
        path.getPathList()
        path.viewPath()
    },
    run: function() {
        document.addEventListener('sectionChanged', this.handleSectionChange.bind(this))  // custom header event
        this.updateCreateButtonsDataset()
    }
}
Header.run()

let content = {
    notes: null,  // dict of notes
    noteFolders: null,  // dict of note folders
    notices: null,  // dict of notices
    noticeFolders: null,  // dict of notice folders
    notesRoot: null,  // root folder id
    noticesRoot: null,  // root folder id

    Note: function({pk, title, folder_id, color, changed_at, description}) {  // create note object using new notation
        this.id = parseInt(pk)
        this.title = title
        this.parent_id = parseInt(folder_id)  // folder id
        this.color = color
        this.changed_at = changed_at
        this.description = description || ''
    },
    Notice: function({pk, title, folder_id, color, changed_at, description, next_date, time, period}) {  // create notice object using new notation
        this.id = parseInt(pk)
        this.title = title
        this.parent_id = parseInt(folder_id)  // folder id
        this.color = color
        this.changed_at = changed_at
        this.description = description || ''
        this.date = next_date
        this.time = time
        this.period = period
    },
    Folder: function({pk, parent_id, title, color, changed_at, children}) {  // create folder object using new notation
        this.folder_id = parseInt(pk)
        this.parent_id = parent_id === null ? null : parseInt(parent_id)
        this.title = title
        this.color = color
        this.changed_at = changed_at
        this.children = children  // str of object ids like 'f9,f10,n7,n9,n5,n4,n12'
    },

    getContentAJAX: async function(url) {  // getting FS content from server
        // получение уведомлений также будет через эту функцию (отдельным запросом)
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
            console.log(`Контент получен`)
        }
    
        return response
    },
    getListOfObjects: async function() {  // creating Objects by templates from above
        const recordContentUrl = conf.Domains['server'] + conf.Urls['getFileSystem']
        const noticeContentUrl = conf.Domains['server'] + conf.Urls['getFileSystemNotice']

        const {folders: recordFolders, records: records} = await this.getContentAJAX(recordContentUrl)
        const {folders: noticeFolders, notices: notices} = await this.getContentAJAX(noticeContentUrl)

        const listOfRecordObjects = []
        for (let i=0;i<records.length;i++) {
            listOfRecordObjects.push(new this.Note(records[i]))
        }

        const listOfRecordFolderObjects = []
        for (let i=0;i<recordFolders.length;i++) {
            listOfRecordFolderObjects.push(new this.Folder(recordFolders[i]))
        }

        const listOfNoticeObjects = []
        for (let i=0;i<notices.length;i++) {
            listOfNoticeObjects.push(new this.Notice(notices[i]))  // проверить конструктор Notice
        }

        const listOfNoticeFolderObjects = []
        for (let i=0;i<noticeFolders.length;i++) {
            listOfNoticeFolderObjects.push(new this.Folder(noticeFolders[i]))  // проверить конструктор Folder
        }

        return {
            notesList: listOfRecordObjects,
            noteFoldersList: listOfRecordFolderObjects,
            noticesList: listOfNoticeObjects,
            noticeFoldersList: listOfNoticeFolderObjects,
        }

    },
    getDictOfRecords: function(listOfRecords) {  // getting dictionary of records by id
        let record_dict = {}
        for (let record_i=0; record_i < listOfRecords.length; record_i++) {
            record_dict[listOfRecords[record_i].id] = listOfRecords[record_i]
        }
        return record_dict
    },
    getDictOfFolders: function(listOfFolders) {  // Getting dictionary of folders by folder_id. Has the following form:
        // folder_dict = {
        //     folder_id:{
        //         folders:[...], - IDs of folders inside the folder with folder_id
        //         objects:[...], - IDs of objects (notes/notices) inside the folder with folder_id
        //         info - information about the folder with folder_id
        //     }, 
        //     ...
        // }
        let folderDict = {}
        for (let folder_i=0; folder_i < listOfFolders.length; folder_i++) {
            folderDict[listOfFolders[folder_i].folder_id] = {
                folders: [],
                objects: [],
                info: listOfFolders[folder_i]
            }

            let children = listOfFolders[folder_i].children
            if (children) {  // если children не пустая строка
                let childrenList = children.split(',')
                for (let i=0; i<childrenList.length;i++) {
                    if (childrenList[i][0]==='f') {
                        folderDict[listOfFolders[folder_i].folder_id].folders.push(childrenList[i])
                    } else if (childrenList[i][0]==='n') {
                        folderDict[listOfFolders[folder_i].folder_id].objects.push(childrenList[i])
                    }
                }
            } 

        }
        return folderDict
    },
    getContent: async function() {  // getting all content (records, notices and folders) from the server
        const {
            notesList: notesList, noteFoldersList: noteFoldersList,  // notes
            noticesList: noticesList, noticeFoldersList: noticeFoldersList,  // notices
        } = await this.getListOfObjects()

        let notesDict = this.getDictOfRecords(notesList)
        let noteFoldersDict = this.getDictOfFolders(noteFoldersList)
        let noticesDict = this.getDictOfRecords(noticesList)
        let noticeFoldersDict = this.getDictOfFolders(noticeFoldersList)
        
        this.notes = notesDict
        this.noteFolders = noteFoldersDict
        this.notices = noticesDict
        this.noticeFolders = noticeFoldersDict

        this.notesRoot = noteFoldersList.find(f => f.parent_id === null).folder_id
        this.noticesRoot = noticeFoldersList.find(f => f.parent_id === null).folder_id
    },

    change: {  // changes existing objects (using and without AJAX)
        addNote: function({pk, title, folder_id, color, changed_at, description}) {  // creation a new record (ajax in form.createRecord)
            const newNote = new content.Note({pk, title, folder_id, color: conf.colors.forward[color], changed_at, description})
            content.notes[newNote.id] = newNote
            const folder = content.noteFolders[folder_id]
            folder.objects.push('n'+pk)
            folder.info['children'] = folder.folders.join(',') + ',' + folder.objects.join(',')

            viewContent.removeObjects()
            viewContent.displayItems()
        },
        delNote: async function(id) {  // deletion the record (including ajax)

            const url = conf.Domains['server'] + conf.Urls.FSRecord(id)
            const options = {
                method: 'DELETE',
                headers: {
                    'Content-Type': 'application/json',
                },
                credentials: 'include',
            }
            const response = await conf.AJAX.send(url, options)
            
            if (response === undefined) {
                console.log(`Error: неопознанная ошибка при удалении записи`)
                return false
            }
            
            if (response === 'Заметка успешно удалена') {
                const parentId = content.notes[id].parent_id
                const parentFolder = content.noteFolders[parentId]
                const recordIndex = parentFolder.objects.indexOf('n' + id)
                if (recordIndex > -1) {
                    parentFolder.objects.splice(recordIndex, 1)
                }
                delete content.notes[id]
                parentFolder.info['children'] = parentFolder.folders.join(',') + ',' + parentFolder.objects.join(',')
                
                viewContent.removeObjects()
                viewContent.displayItems()
                
                console.log(`Запись id=${id} удалена`)
                return true
            }
            return false
        },
        addNoteFolder: function({pk, parent_id, title, color, changed_at, children}) {  // creation a new record folder (ajax in form.createFolder)
            const newFolder = new content.Folder(
                {pk, title, parent_id, color: conf.colors.forward[color], changed_at, children})
            content.noteFolders[newFolder.folder_id] = {
                folders: [],
                objects: [],
                info: newFolder
            }

            const parentFolder = content.noteFolders[parent_id]
            parentFolder.folders.push('f' + pk)
            parentFolder.info['children'] = parentFolder.folders.join(',') + ',' + parentFolder.objects.join(',')

            viewContent.removeObjects()
            viewContent.displayItems()
        },
        delNoteFolder: async function(id) {  // deletion the record folder (including ajax)
            const url = conf.Domains['server'] + conf.Urls.FSFolder(id)
            const options = {
                method: 'DELETE',
                headers: {
                    'Content-Type': 'application/json',
                },
                credentials: 'include',
            }
            const response = await conf.AJAX.send(url, options)
            
            if (response === undefined) {
                console.log(`Error: неопознанная ошибка при удалении папки`)
                return false
            }
            
            if (response === 'Папка успешно удалена' || response) {
                const parentId = content.noteFolders[id].info.parent_id
                const parentFolder = content.noteFolders[parentId]
                const folderIndex = parentFolder.folders.indexOf('f' + id)
                if (folderIndex > -1) {
                    parentFolder.folders.splice(folderIndex, 1)
                }
                delete content.noteFolders[id]
                parentFolder.info['children'] = parentFolder.folders.join(',') + ',' + parentFolder.objects.join(',')
                
                viewContent.removeObjects()
                viewContent.displayItems()
                
                console.log(`Папка id=${id} удалена`)
                return true
            }
            return false
        },
        addNotice: function({pk, title, folder_id, color, changed_at, description, next_date, time}) {  // creation a new notice (ajax in form.createNotice)
            const newNotice = new content.Notice({pk, title, folder_id, color: conf.colors.forward[color], changed_at, description, next_date, time})
            content.notices[newNotice.id] = newNotice
            const folder = content.noticeFolders[folder_id]
            folder.objects.push('n'+pk)
            folder.info['children'] = folder.folders.join(',') + ',' + folder.objects.join(',')

            viewContent.removeObjects()
            viewContent.displayItems()
        },
        delNotice: async function(id) {  // deletion the notice (including ajax)
            const url = conf.Domains['server'] + conf.Urls.FSNotice(id)
            const options = {
                method: 'DELETE',
                headers: {
                    'Content-Type': 'application/json',
                },
                credentials: 'include',
            }
            const response = await conf.AJAX.send(url, options)
            
            if (response === undefined) {
                console.log(`Error: неопознанная ошибка при удалении напоминания`)
                return false
            }
            
            if (response === 'Напоминание успешно удалено' || response) {
                const parentId = content.notices[id].parent_id
                const parentFolder = content.noticeFolders[parentId]
                const recordIndex = parentFolder.objects.indexOf('n' + id)
                if (recordIndex > -1) {
                    parentFolder.objects.splice(recordIndex, 1)
                }
                delete content.notices[id]
                parentFolder.info['children'] = parentFolder.folders.join(',') + ',' + parentFolder.objects.join(',')
                
                viewContent.removeObjects()
                viewContent.displayItems()
                
                console.log(`Напоминание id=${id} удалено`)
                return true
            }
            return false
        },
        addNoticeFolder: function({pk, parent_id, title, color, changed_at, children}) {  // creation a new notice folder (ajax in form.createNoticeFolder)
            const newFolder = new content.Folder(
                {pk, title, parent_id, color: conf.colors.forward[color], changed_at, children})
            content.noticeFolders[newFolder.folder_id] = {
                folders: [],
                objects: [],
                info: newFolder
            }

            const parentFolder = content.noticeFolders[parent_id]
            parentFolder.folders.push('f' + pk)
            parentFolder.info['children'] = parentFolder.folders.join(',') + ',' + parentFolder.objects.join(',')

            viewContent.removeObjects()
            viewContent.displayItems()
        },
        delNoticeFolder: async function(id) {  // deletion the notice folder (including ajax)
            const url = conf.Domains['server'] + conf.Urls.FSFolderNotice(id)
            const options = {
                method: 'DELETE',
                headers: {
                    'Content-Type': 'application/json',
                },
                credentials: 'include',
            }
            const response = await conf.AJAX.send(url, options)
            
            if (response === undefined) {
                console.log(`Error: неопознанная ошибка при удалении папки напоминания`)
                return false
            }
            
            if (response === 'Папка успешно удалена' || response) {
                const parentId = content.noticeFolders[id].info.parent_id
                const parentFolder = content.noticeFolders[parentId]
                const folderIndex = parentFolder.folders.indexOf('f' + id)
                if (folderIndex > -1) {
                    parentFolder.folders.splice(folderIndex, 1)
                }
                delete content.noticeFolders[id]
                parentFolder.info['children'] = parentFolder.folders.join(',') + ',' + parentFolder.objects.join(',')
                
                viewContent.removeObjects()
                viewContent.displayItems()
                
                console.log(`Папка напоминания id=${id} удалена`)
                return true
            }
            return false
        },
    },

    run: async function() {
        await this.getContent()
    }
}
await content.run()

let viewContent = {
    // currentType: null,
    currentFolderId: null,
    
    displayItems: function() {  // display all DAD-objects
        // отображение должно подождать завершения ajax запроса контента!!!!!!!
        let foldersDict, recordsDict, foldersIdList,recordsIdList, isRoot
        if (session.section === 'notes') {
            foldersDict = content.noteFolders
            recordsDict = content.notes
            foldersIdList = Array.from(content.noteFolders[this.currentFolderId].folders)
            for (let i=0; i<foldersIdList.length;i++) {
                foldersIdList[i] = foldersIdList[i].slice(1,)
            }
            recordsIdList = Array.from(content.noteFolders[this.currentFolderId].objects)
            for (let i=0; i<recordsIdList.length;i++) {
                recordsIdList[i] = recordsIdList[i].slice(1,)
            }
        } else if (session.section === 'notices') {
            foldersDict = content.noticeFolders
            recordsDict = content.notices
            foldersIdList = Array.from(content.noticeFolders[this.currentFolderId].folders)
            for (let i=0; i<foldersIdList.length;i++) {
                foldersIdList[i] = foldersIdList[i].slice(1,)
            }
            recordsIdList = Array.from(content.noticeFolders[this.currentFolderId].objects)
            for (let i=0; i<recordsIdList.length;i++) {
                recordsIdList[i] = recordsIdList[i].slice(1,)
            }
        } else {
            console.log('viewContent Error: records type doesnt exist')
        }

        // display back-folder
        let parent_id = foldersDict[this.currentFolderId].info.parent_id
        if (parent_id !== null) {
            this.createBackFolder(parent_id)
        }

        for (let i=0; i<foldersIdList.length; i++) {
            // console.log('foldersDict', foldersDict)
            // console.log('foldersDict[foldersIdList[i]]', foldersDict[foldersIdList[i]])
            // console.log('foldersIdList[i]', foldersIdList[i])
            this.createObject(
                foldersDict[foldersIdList[i]].info.folder_id,  // id
                foldersDict[foldersIdList[i]].info.title,  // title
                null,  // labels
                foldersDict[foldersIdList[i]].info.color,  // color
                DADSettings.folderClass,  // objtype
            )
        }
        for (let i=0; i<recordsIdList.length; i++) {
            this.createObject(
                recordsDict[recordsIdList[i]].id,  // id
                recordsDict[recordsIdList[i]].title,  // title
                null,  // labels
                recordsDict[recordsIdList[i]].color,  // color
                DADSettings.recordClass,  // objtype
                recordsDict[recordsIdList[i]].date+' '+recordsDict[recordsIdList[i]].time  // datetime
            )
        }

    },
    createBackFolder: function(parent_id) {  // display object to return to the parent folder
        let block = document.createElement("div")
        let titleP = document.createElement("p")
        block.classList.add(classNames.backFolder)
        block.classList.add(DADSettings.folderClass)
        block.id = parent_id
        titleP.textContent = 'Вернуться...'
        objectsList.append(block)
        block.append(titleP)
    },
    createObject: function(id, title, labelsList, color, objtype, datetime) {  // create any DAD-object

        let isNotices = session.section==='notices'
        let isRecord = objtype===DADSettings.recordClass

        let noteBlock = document.createElement("div")
        let blockRow = document.createElement("div")
        let coll1 = document.createElement("div")
            let marker = document.createElement("div")
            // svg
        let coll2 = document.createElement("div")
            let datetimeObj, datetimeP, space
            if (isNotices&&isRecord) {
                datetimeObj = document.createElement("div")
                datetimeP = document.createElement("div")
                space = document.createElement("span")
            }
            
            let titleBlock = document.createElement("div")
                let titleP = document.createElement("p")
        let coll3 = document.createElement("div")
            let labels = document.createElement("div")
            // svg

        // noteBlock.className = "dd-object"
        noteBlock.classList.add('dd-object')
        noteBlock.classList.add('draggableObject')
        if (isRecord) {
            noteBlock.classList.add(DADSettings.recordClass)
        } else {
            noteBlock.classList.add(DADSettings.folderClass)
        }
        noteBlock.id = id
        blockRow.className = 'block-row'
        coll1.className = 'coll1'
        coll2.className = 'coll2'
        coll3.className = 'coll3'
        marker.className = 'marker'
        marker.dataset['color'] = conf.colors.revers[color]
        if (isNotices&&isRecord) {
            datetimeObj.className = 'datetime'
            datetimeP.textContent = datetime
            space.textContent = ' — '
        }
        titleBlock.className = 'title'
        titleP.textContent = title
        labels.className = 'labels'
        // labels.textContent = 'labels'

        objectsList.append(noteBlock)
        noteBlock.append(blockRow)
        blockRow.append(coll1, coll2, coll3)
        coll1.append(marker)
        if (isNotices&&isRecord) {
            coll2.append(datetimeObj)
            datetimeObj.append(datetimeP)
            coll2.append(space)
        }
        coll2.append(titleBlock)
        titleBlock.append(titleP)
        // coll3.append(labels)

        if (isRecord) {
            this.createSVG(  // type
                coll1,  // parent
                'content-svg',  // className
                '2 0 20 24',  // viewBox
                [  // pathLst
                    'm7 12h10v2h-10zm0 6h7v-2h-7zm15-10.414v16.414h-20v-21a3 3 0 0 1 3-3h9.414zm-7-.586h3.586l-3.586-3.586zm5 15v-13h-7v-7h-8a1 1 0 0 0 -1 1v19z',
                ]
            )
        }

        if (!isRecord) {
            this.createSVG(  // type
                coll1,  // parent
                'content-svg',  // className
                '0 0 24 24',  // viewBox
                [  // pathLst
                    'M21,3H12.236l-4-2H3A3,3,0,0,0,0,4V23H24V6A3,3,0,0,0,21,3ZM3,3H7.764l4,2H21a1,1,0,0,1,1,1v.881L2,6.994V4A1,1,0,0,1,3,3ZM2,21V8.994l20-.113V21Z',
                ]
            )
        }
        
        this.createSVG(  // settings
            coll3,  // parent
            'content-svg',  // className
            '0 0 24 24',  // viewBox
            [  // pathLst
                'M12,8a4,4,0,1,0,4,4A4,4,0,0,0,12,8Zm0,6a2,2,0,1,1,2-2A2,2,0,0,1,12,14Z',
                'M21.294,13.9l-.444-.256a9.1,9.1,0,0,0,0-3.29l.444-.256a3,3,0,1,0-3-5.2l-.445.257A8.977,8.977,0,0,0,15,3.513V3A3,3,0,0,0,9,3v.513A8.977,8.977,0,0,0,6.152,5.159L5.705,4.9a3,3,0,0,0-3,5.2l.444.256a9.1,9.1,0,0,0,0,3.29l-.444.256a3,3,0,1,0,3,5.2l.445-.257A8.977,8.977,0,0,0,9,20.487V21a3,3,0,0,0,6,0v-.513a8.977,8.977,0,0,0,2.848-1.646l.447.258a3,3,0,0,0,3-5.2Zm-2.548-3.776a7.048,7.048,0,0,1,0,3.75,1,1,0,0,0,.464,1.133l1.084.626a1,1,0,0,1-1,1.733l-1.086-.628a1,1,0,0,0-1.215.165,6.984,6.984,0,0,1-3.243,1.875,1,1,0,0,0-.751.969V21a1,1,0,0,1-2,0V19.748a1,1,0,0,0-.751-.969A6.984,6.984,0,0,1,7.006,16.9a1,1,0,0,0-1.215-.165l-1.084.627a1,1,0,1,1-1-1.732l1.084-.626a1,1,0,0,0,.464-1.133,7.048,7.048,0,0,1,0-3.75A1,1,0,0,0,4.79,8.992L3.706,8.366a1,1,0,0,1,1-1.733l1.086.628A1,1,0,0,0,7.006,7.1a6.984,6.984,0,0,1,3.243-1.875A1,1,0,0,0,11,4.252V3a1,1,0,0,1,2,0V4.252a1,1,0,0,0,.751.969A6.984,6.984,0,0,1,16.994,7.1a1,1,0,0,0,1.215.165l1.084-.627a1,1,0,1,1,1,1.732l-1.084.626A1,1,0,0,0,18.746,10.125Z'
            ]
        )
    },
    createSVG: function(parent, className, viewBox, pathLst) {  // create svg elements
        let svg = document.createElementNS("http://www.w3.org/2000/svg", "svg")
        svg.setAttributeNS(null, 'class', className)
        svg.setAttributeNS(null, 'viewBox', viewBox)
        for (let i=0; i < pathLst.length; i++) {
            let svgPath = document.createElementNS("http://www.w3.org/2000/svg", 'path')
            svgPath.setAttributeNS(null, 'd', pathLst[i])
            svg.appendChild(svgPath)
        }
        parent.append(svg)
        // https://ru.stackoverflow.com/questions/1123250/%D0%9A%D0%B0%D0%BA-%D0%B2%D1%81%D1%82%D0%B0%D0%B2%D0%B8%D1%82%D1%8C-svg-%D0%BA%D0%BE%D0%B4-%D0%BD%D0%B0-%D1%81%D0%B0%D0%B9%D1%82-%D1%81-%D0%BF%D0%BE%D0%BC%D0%BE%D1%89%D1%8C%D1%8E-js    
    },
    removeObjects: function() { // clean DAD-area, delete all DAD-objects
        let objectsList = document.getElementById('objectsList')
        objectsList.innerHTML = ''
    },
    openObject: function(event) { // open record or folder or back-folder
        // функция обрабатывает нажатия в обоих режимах (notes/notices)!!!
        if (mobileSettings.device === 'desktop' && !DragAndDrop.isClick) return
        let isDDobject = event.target.closest('.dd-object')
        let isBackFolder = event.target.closest(`.${classNames.backFolder}`)
        if (!(isDDobject || isBackFolder)) return
        
        let folder = event.target.closest('.folder')
        let record = event.target.closest('.record')
        if (folder) {
            this.openFolder(folder.id)
        }
        if (record) {
            this.openRecord(record.id)
        }
    },
    openFolder: function(folder_id) { // opening the folder
        this.currentFolderId = folder_id
        viewContent.removeObjects()
        viewContent.displayItems()
        path.getPathList()
        path.viewPath()
    },
    openRecord: function(record_id) { // opening the records
        // данная функция открывает и record, и notice!!!
        // console.log('Переход на страницу записи ', session.section,' типа, id=', record_id)
        const section = session.section === 'notices' ? 'notices' : 'notes'
        window.location.href = `/${section}/${record_id}/`
    },
    run: function() {
        if (session.section == 'notes') {
            this.currentFolderId = content.notesRoot
        } else {
            this.currentFolderId = content.noticesRoot
        }
        this.removeObjects()
        this.displayItems() // отображение должно подождать завершения ajax запроса контента!!!!!!!
        let ddArea = document.getElementById('objectsList')
        ddArea.addEventListener('click', this.openObject.bind(this))
    }
}
viewContent.run()

let path = {  // Directory of folders at the top 
    pathList: [], // list of objects like [{name, id},...]

    getPathList: function() {  // generate list of folder path for directory

        this.pathList = []
        let parentId = viewContent.currentFolderId
        let currentFolderType
        if (session.section==='notes') {
            currentFolderType = content.noteFolders
        } else if (session.section==='notices') {
            currentFolderType = content.noticeFolders
        }
        this.pathList.unshift({  // Current folder
            name: currentFolderType[parentId].info.title,
            id: parentId
        })

        while (parentId != null) {  // other elems
            parentId = currentFolderType[parentId].info.parent_id
            if (parentId === null) break
            this.pathList.unshift({
                name: currentFolderType[parentId].info.title,
                id: parentId
            })
        }
        if (this.pathList[0]) { // First folder (section)
            if (session.section==='notes') {
                this.pathList[0].name = 'Заметки'
            } else if (session.section==='notices') {
                this.pathList[0].name = 'Напоминания'
            }
        }
    },
    viewPath: function() {  // display directory
        let path = document.getElementById('path')
        path.innerHTML = ''
        for (let i=0; i<this.pathList.length; i++) {
            if (i>0) {
                let delimiter = document.createElement('span')
                delimiter.className = 'path-delimiter'
                delimiter.textContent = ' / '
                path.append(delimiter)
            }

            let pathFolder = document.createElement('div')
            pathFolder.className = 'path-folder'
            pathFolder.textContent = this.pathList[i].name
            path.append(pathFolder)
        }
    },
    getPath: function(event) {  // open the folder using the directory by click
        if (event.target.className != 'path-folder') return
        let newFolderId
        for (let i=0; i<this.pathList.length; i++) {
            if (this.pathList[i].name === event.target.textContent) {
                newFolderId = this.pathList[i].id
            }
        }
        viewContent.openFolder(newFolderId)
    },
    run: function() {
        this.getPathList()
        this.viewPath()
        let path = document.getElementById('path')
        path.addEventListener('click', this.getPath.bind(this))
    }
}
path.run()

let DragAndDrop = {
    DADObject: {  // Properties of the selected dragging Object
        "typeObject": null,  // record or folder
        "object": null,  // the object itself
        "text": null
    },
    stickyDAD: null,  // Drag And Drop HTML Object attached to mouse (pointer)
    
    // мы будем запомним элемент и расположение курсора (четверть) 
    // в Move-событии для обработки End-события
    draggingVariables: {
        "dragRelocate": null, // Элемент, над которым был курсор при перемещении объекта
        "dragRelocateQuarter": null, // четверть, над которым был курсор при перемещении объекта (1 или 4)
        "dragPutInside": null // папка, в которую был помещен объект
    },

    // переменная, необходимая для запоминания элемента, с которого ушел курсор
    // это необходимо для снятия выделения ячейки
    // event.target и event.relatedTarget почему-то на телефоне не работают - см. примечание
    leaveObjects: {
        "previous": null,
        "next": null
    },

    isClick: false, // включает в down, выключается в move (для вхождения в папку)

    //////////////////////////////////////////////////////////////////////
    // Mouse PRESS events
    //////////////////////////////////////////////////////////////////////
    pointerDownEvent: function(event) {  // click the draggable object
        if (mobileSettings.device === 'mobile' && mobileSettings.DAD === false) return // DAD must be true using mobile
        let isFolder = document.elementFromPoint(event.clientX, event.clientY).closest(`.${DADSettings.folderClass}`)
        let isRecord = document.elementFromPoint(event.clientX, event.clientY).closest(`.${DADSettings.recordClass}`)
        if ((isFolder??isRecord)&&event.which != 3) {
            this.isClick = true  // вхождение в папку
        }
        
        if (!this.pointerDownEventChecks(event)) {  // проверки на срабатывание DAD
            return
        }
        if (!this.getDADObject(event)) {  // Создание DADObject
            return
        }

        window.getSelection().removeAllRanges()  // disable all selection during DD
        
        this.enableSelected(this.DADObject.object)
        
        let stickyDADCoord = this.getStickyDADCoord(event.clientX, event.clientY) // координаты stickyDAD объекта {x, y}
        this.createDADIcon(stickyDADCoord.left, stickyDADCoord.top)  // создаем блок-подсказку, приклеенный к мыши

        this.leaveObjects.next = this.DADObject.object  // для работы снятия выделения в pointerMoveEvent

    },
    pointerDownEventChecks: function(event) {  // any checks for DAD start
        if (event.which != 1) {  // DAD работает только при нажатии левой кнопки мыши (или пальцем на экран телефона)
            if (document.body.contains(this.stickyDAD)) {  // удаляем существующие объекты при нажатии не левой кнопки
                this.disableSelected(this.DADObject.object)
                document.body.removeChild(this.stickyDAD)
                this.stickyDAD = undefined
            }
            return false
        }
    
        // DAD (нажатие мыши) не срабатывает на папку "вернуться"
        let isBackFolder = document.elementFromPoint(event.clientX, event.clientY).closest(`.${DADSettings.folderClass}.${classNames.backFolder}`)
        if (isBackFolder) {
            return false
        }
        // DAD (нажатие мыши) не срабатывает, если нажимать на область с настройками
        let isSettingField = document.elementFromPoint(event.clientX, event.clientY).closest(`.${classNames.settingIcon}`)
        if (isSettingField) {
            return false
        }
        return true
    },
    getDADObject: function(event) {  // getting DAD-object
        // Определяем, на каком объекте произошло нажатие. получаем объект dADObject
        let folderUnderCursorHTML = document.elementFromPoint(event.clientX, event.clientY).closest(`.${DADSettings.folderClass}`)
        let recordUnderCursorHTML = document.elementFromPoint(event.clientX, event.clientY).closest(`.${DADSettings.recordClass}`)
        if (folderUnderCursorHTML) {
            this.DADObject = {
                "typeObject": `${DADSettings.folderClass}`,
                "object": folderUnderCursorHTML,
                "text": folderUnderCursorHTML.querySelector(`.folder .title p`).textContent
            }
        } else if (recordUnderCursorHTML) {
            this.DADObject = {
                "typeObject": `${DADSettings.recordClass}`,
                "object": recordUnderCursorHTML,
                "text": recordUnderCursorHTML.querySelector(`.record .title p`).textContent
            }
        } else { // никакой объект под мышкой не найден
            return false
        }
        return true
    },
    getStickyDADCoord: function(pointerX, pointerY) {  // getting coords for stickyObject
        // объект не должен визуально выходить за границы области

        // координаты DAD области
        let objectsList = document.getElementById('objectsList')
        let bounds = objectsList.getBoundingClientRect()
        let directMenuCoord = {
            "left_start": bounds.x,
            "left_end": bounds.x + bounds.width,
            "top_start": bounds.y,
            "top_end": bounds.y + bounds.height,
        }

        let stickyDADCoord = { // координаты закрепленного DAD объекта
            "left": pointerX,
            "top": pointerY
        }

        // смещение закрепленного объекта на границах DAD-area
        if (pointerX < directMenuCoord.left_start) {  // Оx
            stickyDADCoord.left = directMenuCoord.left_start
        } else if (pointerX > (directMenuCoord.left_end - stickyDADSettings.width)) {
            stickyDADCoord.left = directMenuCoord.left_end - stickyDADSettings.width
        } else {
            stickyDADCoord.left = pointerX
        }
        if (pointerY < directMenuCoord.top_start) {  // Oy
            stickyDADCoord.top = directMenuCoord.top_start
        } else if (pointerY > (directMenuCoord.top_end - stickyDADSettings.height)) {
            stickyDADCoord.top = directMenuCoord.top_end - stickyDADSettings.height
        } else {
            stickyDADCoord.top = pointerY
        }
        stickyDADCoord.top += window.pageYOffset  // смещение вниз при перемещении скролла
        return stickyDADCoord
    },
    createDADIcon: function(left, top) {  // create an object attached to the mouse
        if (this.stickyDAD !== null) {  // Если объект уже существует, то новый не создаем (защита от багов)
            return
        }
    
        this.stickyDAD = document.createElement("div") // создаем блок-подсказку, закрепленный за мышкой, вручную
        this.stickyDAD.className = classNames.stickyDAD
        this.stickyDAD.id = 'stickyDAD'
        this.stickyDAD.innerHTML = `
            <div class="dragging-object" id="dragging_object" style="width: ${stickyDADSettings.width}px; height: ${stickyDADSettings.height}px; border: solid rgb(0, 0, 0) 2px; border-radius: 5px;">
                <p style="margin-bottom: 0px">${this.DADObject.text}</p>
            </div>
        `
        this.stickyDAD.style.position = 'absolute'
        this.stickyDAD.style.zIndex = 1000
        this.stickyDAD.style['pointer-events'] = "none"  // запрещает объекту реагировать на мышь
        this.stickyDAD.style.left = left + "px"  // создаем объект под мышью
        this.stickyDAD.style.top = top + "px"
    
        let dragging_object = this.stickyDAD.children.item(0)
        dragging_object.style['background-color'] = 'antiquewhite'
        dragging_object.style['border-color'] = stickyDADSettings['border-color']
        dragging_object.style.opacity = stickyDADSettings.opacity
    
        // document.body.append(this.stickyDAD)

    },
    enableSelected(obj) {  // object selection during DAD
        obj.style['background-color'] = 'grey'
    },
    disableSelected(obj) {  // disable object selection during DAD
        obj.style['background-color'] = null
    },
    disableRightButton: function(event) { // disable right btn during DD
        if (!(this.isClick || this.DADObject.object)) {
            return
        }
        event.preventDefault()
    },

    //////////////////////////////////////////////////////////////////////
    // Mouse MOVE events
    //////////////////////////////////////////////////////////////////////
    pointerMoveEvent: function(event) {  // main movement event

        if (this.stickyDAD !== null) {  // attach sticky object to mouse
            let stickyDADCoord = this.getStickyDADCoord(event.clientX, event.clientY) // координаты stickyDAD объекта {x, y}
            this.stickyDAD.style.left = stickyDADCoord.left + "px"
            this.stickyDAD.style.top = stickyDADCoord.top + "px"
            document.body.append(this.stickyDAD)
        }
        this.isClick = false // disable transition into the folder during DAD
        if (!this.DADObject.object) return  // Does DAD-object exist?

        // Находим элемент, над которым в данный момент находится курсор (папка или запись)
        let elementBelow = document.elementFromPoint(event.clientX, event.clientY).closest(`.${DADSettings.draggableClass}`)
        elementBelow = elementBelow?
            elementBelow:
            document.elementFromPoint(event.clientX, event.clientY).closest(`.${classNames.backFolder}`)

        if (!this.checkDraggingElem(elementBelow)) {
            // Курсор не над папкой/записью (например, в margin между элементами)
            // Сбрасываем dragPutInside, чтобы при отпускании не переместить в папку
            this.draggingVariables.dragPutInside = null
            return  // Does event correct?
        }
        
        // Проверяем, что курсор действительно находится внутри границ элемента (не в margin между элементами)
        if (!this.isCursorInsideElement(event.clientX, event.clientY, elementBelow)) {
            // Курсор находится в margin между элементами, сбрасываем dragPutInside
            this.draggingVariables.dragPutInside = null
            return
        }
        // определяем, в какой зоне (верх, середина, низ) над проносимымы объектом находится курсор
        let relativePosition = this.getRelativePosition(event, elementBelow)

        // если под нами папка "вернуться", то элемент нельзя переместить выше нее
        // если папка не будет перечисленная в общем списке, то зоны не имеют значения (будет только "переместить внутрь")
        let backFolder = document.getElementsByClassName('folder-back')[0]
        if ((elementBelow == backFolder) && ['top', 'middle'].includes(relativePosition)) {
            this.draggingPutInsideFolder(elementBelow)
            return
        }
        
        // мы перетаскиваем папку или запись (с зажатой ЛКМ)
        if (this.DADObject.object.classList.contains(DADSettings.folderClass)) {
            this.draggingFolder(event, elementBelow, relativePosition)
        } else if (this.DADObject.object.classList.contains(DADSettings.recordClass)) {
            this.draggingRecord(event, elementBelow, relativePosition)
        } else {
            console.log('The object under the cursor is not recognized as a folder or record')
        }
    },
    checkDraggingElem: function(elementBelow) { // check of correctness of the operation
        if (!elementBelow) {
            return false
        }
        let belowIsFolder = elementBelow.classList.contains(`${DADSettings.folderClass}`)
        let belowIsRecord = elementBelow.classList.contains(`${DADSettings.recordClass}`)
        if (this.DADObject !== elementBelow &&  // событие сработало не на том элементе, который мы перемещаем
            (belowIsFolder || belowIsRecord)) // событие сработало именно на элементе списка папок и записей
        { return true } else 
        { return false }
    },
    isCursorInsideElement: function(cursorX, cursorY, element) { // проверка, что курсор находится внутри границ элемента
        if (!element) return false
        const rect = element.getBoundingClientRect()
        return (
            cursorX >= rect.left &&
            cursorX <= rect.right &&
            cursorY >= rect.top &&
            cursorY <= rect.bottom
        )
    },
    getRelativePosition: function(event, elementBelow) {  // searching for relative cursor position
        let elementCoord = elementBelow.getBoundingClientRect();
        let relativeY = event.clientY - elementCoord.y // координата Y относительно начала элемента (сверху вниз)
        let absoluteY = elementCoord.height // координата Y элемента (его высота)

        // Every element is divided into 3 zones: top, miggle, bottom
        if (relativeY <= DADSettings.putBeetwenArea) {
            return 'top'
        } else if (relativeY <= absoluteY - DADSettings.putBeetwenArea) {
            return 'middle'
        } else if (relativeY <= absoluteY) {
            return 'bottom'
        } else if (
            // произошло смещение элемента и координаты "прошлого" элемента изменились
            document.elementFromPoint(event.clientX, event.clientY).closest(`.${DADSettings.folderClass}`) &&
            elementBelow == document.elementFromPoint(event.clientX, event.clientY).closest(`.${DADSettings.folderClass}`).previousElementSibling
        ) {
            return false
        } else {
            console.log('Error of getRelativePosition()')
            return false
        }
    },
    draggingFolder: function(event, elementBelow, relativePosition) {  // dragging folder
        let belowIsFolder = elementBelow.classList.contains(DADSettings.folderClass)
        if (['middle'].includes(relativePosition) && belowIsFolder) {
            this.draggingPutInsideFolder(elementBelow, relativePosition)
        } else if (['top', 'bottom'].includes(relativePosition) && belowIsFolder) {
            if (!(this.DADObject.object === elementBelow)) {
                this.disableSelected(elementBelow)  // снятие выделения при перемещении из 2/4 и 3/4
            }
            this.draggingInsertElement(event, elementBelow, relativePosition)
        }
    },
    draggingRecord: function(event, elementBelow, relativePosition) {  // dragging record
        let belowIsFolder = elementBelow.classList.contains(DADSettings.folderClass)
        if (belowIsFolder) {
            this.draggingPutInsideFolder(elementBelow, relativePosition)
        } else {
            this.draggingInsertElement(event, elementBelow, relativePosition)
        }
    },
    draggingInsertElement: function(event, elementBelow, relativePosition) {  // inserting between

        // Находим элемент, с которым будем меняться местами
        let beforeElement = this.getBeforeElement(event.clientY, elementBelow)
    
        // Проверяем, нужно ли менять элементы местами
        if (
            beforeElement && (
                this.DADObject.object === beforeElement.previousElementSibling ||
                this.DADObject.object === beforeElement
            )
        ) {
            // Если нет, выходим из функции, чтобы избежать лишних изменений в DOM
            this.draggingVariables.dragPutInside = null
            return;
        }
    
        // Вставляем DADObject.object перед beforeElement
        if (this.DADObject.object !== elementBelow) {
            this.disableSelected(elementBelow)  // снятие выделения при перемещении из 2/4 и 3/4
        }
    
        // !!! вставка между
        elementBelow.parentNode.insertBefore(this.DADObject.object, beforeElement)
    
        // запомним элемент и четверть для окончания D&D
        this.draggingVariables.dragRelocate = elementBelow  // Элемент, над которым был курсор при перемещении объекта
        this.draggingVariables.dragRelocateQuarter = relativePosition  // четверть, над которым был курсор при перемещении объекта (1 или 4)
        this.draggingVariables.dragPutInside = null  // папка, в которую был помещен объект
    
    },
    draggingPutInsideFolder: function(elementBelow, relativePosition) {  // inserting inside the folder

        // Папка не может быть вложена сама в себя
        if (this.DADObject.typeObject === DADSettings.folderClass &&
            this.DADObject.object.id == elementBelow.id) {
            return
        }

        this.enableSelected(elementBelow)
    
        // !!! вставка внутрь
        // запоминаем папку
        this.draggingVariables.dragRelocate = null  // Элемент, над которым был курсор при перемещении объекта
        this.draggingVariables.dragRelocateQuarter = null  // четверть, над которым был курсор при перемещении объекта (1 или 4)
        this.draggingVariables.dragPutInside = elementBelow  // папка, в которую был помещен объект
    
    },
    getBeforeElement: function(cursorCoordY, elementBelow) {  // getting elem that will be shifted by reason of DAD
        // Находим элемент, с которым будем менять местами во время перетаскивания
    
        // Получаем координаты объекта под курсором
        let elementCoord = elementBelow.getBoundingClientRect()
    
        // Находим вертикальную координату центра текущего элемента (отсчитываем heigth вниз)
        let currentElementCenter = elementCoord.y + elementCoord.height / 2
    
        // выбираем beforeElement. Это будет либо элемент, над которым мы парим, либо следующий (ниже).
        // это необходимо, потому что мы можем вставить элемент только ПЕРЕД выбранным (функция insertBefore)
        let beforeElement = (cursorCoordY < currentElementCenter) ? // Если курсор выше центра элемента
            elementBelow :  // возвращаем текущий элемент
            elementBelow.nextElementSibling  // В ином случае — следующий DOM-элемент
    
        return beforeElement;
    },
    pointerMoveEventOut: function(event) {  // finally event since pointerMoveEvent
        // событие перемещения объекта, которое должно сработать в любом случае после pointerMoveEvent
    
        if (!this.DADObject.object) return  // событие move может сработать где угодно. Нас интересуют только DAD события
    
        let elementBelow = document.elementFromPoint(event.clientX, event.clientY).closest(`.${DADSettings.draggableClass}`)
        elementBelow = elementBelow?
            elementBelow:
            document.elementFromPoint(event.clientX, event.clientY).closest(`.${classNames.backFolder}`)

        if (this.leaveObjects.next != elementBelow) {
            this.leaveObjects.previous = this.leaveObjects.next
            this.leaveObjects.next = elementBelow
    
            if (this.leaveObjects.previous != this.DADObject.object && this.leaveObjects.previous) {
                this.disableSelected(this.leaveObjects.previous)
            }
        }
    
        // if (!elementBelow) {
        //     resetOptions(draggingVariables)  // инфа о соверешнном действии
        // }
        return
    
    },
    
    //////////////////////////////////////////////////////////////////////
    // Mouse RELEASE events
    //////////////////////////////////////////////////////////////////////
    pointerUpEvent: function(event) {  // main pointer up event

        if (!this.DADObject.object) {  // если перемещаемый объект не существует
            return
        }
        if (!this.stickyDAD) {  // если перемещаемый объект не существует
            return
        }
        // let elementBelow = (event.target.closest(`.${DADSettings.folderClass}`)) ?
        //     event.target.closest(`.${DADSettings.folderClass}`):
        //     event.target.closest(`.${DADSettings.recordClass}`)
        // event.target doesn't work using mobile
        let elementBelow = document.elementFromPoint(event.clientX, event.clientY)
        elementBelow = elementBelow.closest(`.${DADSettings.folderClass}`) ?
            elementBelow.closest(`.${DADSettings.folderClass}`):
            elementBelow.closest(`.${DADSettings.recordClass}`)
        this.disableSelected(this.DADObject.object)
        if (elementBelow) {
            this.disableSelected(elementBelow)
        }
    
        if (!this.isClick) {
            if (this.draggingVariables.dragPutInside) {
                // Проверяем, что курсор действительно находится внутри границ папки при отпускании
                if (this.isCursorInsideElement(event.clientX, event.clientY, this.draggingVariables.dragPutInside)) {
                    this.putInsideFolder(this.draggingVariables.dragPutInside)
                } else {
                    // Курсор находится в margin между папками, не перемещаем в папку
                    this.draggingVariables.dragPutInside = null
                }
            } else if (this.draggingVariables.dragRelocate) {
                this.changeOrder()
            } else {
                // console.log("Changes does't exist")
            }
        }
        
        this.removeDADMemory()
    
    },
    removeDADMemory: function() {  // clear information about the completed DAD
        
        if (this.leaveObjects.next) {
            this.disableSelected(this.leaveObjects.next)  // снимаем выделения с объектов
        }
    
        // сбрасываем значения переменных
        this.resetOptions(this.draggingVariables)  // инфа о соверешнном действии
        this.resetOptions(this.DADObject)  // инфа о перемещенном объекте действии
        this.resetOptions(this.leaveObjects)  // инфа о последнем объекте, который пересекала мышь
    
        if (document.body.contains(this.stickyDAD)) {  // разрушаем закрепленный DAD-объект - подсказку под мышью/курсором
            document.body.removeChild(this.stickyDAD)
            this.stickyDAD = null
        }
        if (this.stickyDAD != null) {  // объект создается (pointerdown) и отображается (poitermove) отдельно
            this.stickyDAD = null
        }
    
    },
    resetOptions: function(variable) {  // reset properties for next DAD
        for (let key in variable) {
            variable[key] = null
        }
    },
    resetDADEvent: function(event) {  // reset all changes without ajax and content
        if (!this.DADObject.object) return
        if (event.key != 'Escape') return

        this.disableSelected(this.DADObject.object)
        this.removeDADMemory()

        viewContent.removeObjects()
        viewContent.displayItems()
    },

    //////////////////////////////////////////////////////////////////////
    // Симуляция функций для обработки данных
    //////////////////////////////////////////////////////////////////////
    changeOrder: async function() {  // put any object between another objects
        let objects = this.getProperticeByObjectsList()

        let folder
        if (session.section === 'notes') {
            folder = content.noteFolders[viewContent.currentFolderId]
        } else if (session.section === 'notices') {
            folder = content.noticeFolders[viewContent.currentFolderId]
        }
        folder.objects = objects.newRecordList
        folder.folders = objects.newFolderList
        folder.info.children = objects.newChildren

        console.log(this.DADObject)
        
        // Определяем тип объекта для API с учетом секции
        let objectType = ''
        let nestedList = []
        if (this.DADObject.typeObject === DADSettings.recordClass) {
            // Для записей: 'record' для notes, 'notice' для notices
            objectType = session.section === 'notes' ? 'record' : 'notice'
            // Формируем список ID записей (убираем префикс 'n' и преобразуем в числа)
            nestedList = objects.newRecordList.map(id => parseInt(id.slice(1)))
        } else if (this.DADObject.typeObject === DADSettings.folderClass) {
            // Для папок: 'recordFolder' для notes, 'noticeFolder' для notices
            objectType = session.section === 'notes' ? 'recordFolder' : 'noticeFolder'
            // Формируем список ID папок (убираем префикс 'f' и преобразуем в числа)
            nestedList = objects.newFolderList.map(id => parseInt(id.slice(1)))
        }
        
        let data = {
            type: objectType,
            object_id: parseInt(this.DADObject.object.id),
            folder_id: parseInt(viewContent.currentFolderId),
            nested_list: nestedList,
        }

        // выполняем ajax
        const url = conf.Domains['server'] + conf.Urls.moveBetween
        const options = {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            credentials: 'include',
            body: JSON.stringify(data),
        }
        const response = await conf.AJAX.send(url, options)

        if (response === undefined) {
            console.log(`Error: неопознанная ошибка при изменении порядка`)
            return
        }
        
        if (response.success) {
            console.log('Порядок объектов успешно изменен')
        } else {
            console.log(`Error: ${response.msg || 'Ошибка при изменении порядка'}`)
        }

    },
    getProperticeByObjectsList: function() {  // get folders, records, children using html objectsList
        let objectsList = document.getElementById('objectsList').children
        let newFolderList = []
        let newRecordList = []
        for (let i=0; i<objectsList.length; i++) {
            let isFolder = objectsList[i].classList.contains(DADSettings.folderClass)
            let isRecord = objectsList[i].classList.contains(DADSettings.recordClass)
            let isBackFolder = objectsList[i].classList.contains(classNames.backFolder)
            if (isBackFolder) continue
            if (isFolder) {
                newFolderList.push('f'+String(objectsList[i].id))
            } else if (isRecord) {
                newRecordList.push('n'+String(objectsList[i].id))
            } else {
                console.log('DragAndDrop.changeOrder Error')
            }
        }
        let newChildren = newFolderList.join(',') + ',' + newRecordList.join(',')
        if (newRecordList.length===0) newChildren=newChildren.slice(0,-1)
        let outlet = {
            newFolderList: newFolderList,
            newRecordList: newRecordList, 
            newChildren: newChildren
        }
        return outlet
    },
    putInsideFolder: async function(elementBelow) { // put object (record or folder) in folder
        // verifications
        if (!elementBelow) return
        if (!elementBelow.classList.contains(DADSettings.folderClass)) return
        if (!(elementBelow && this.DADObject.object)) return
        if (this.DADObject.typeObject == DADSettings.folderClass &&
            this.DADObject.object.id == elementBelow.id) {
            return // Folder can't relocate inside itself
        }

        // delete draggable elem from the current folder
        this.DADObject.object.remove()

        // getting new and old folders
        let oldFolder = null, newFolder = null
        if (session.section==='notes') {
            oldFolder = content.noteFolders[viewContent.currentFolderId]
            newFolder = content.noteFolders[elementBelow.id]
        } else if (session.section==='notices') {
            oldFolder = content.noticeFolders[viewContent.currentFolderId]
            newFolder = content.noticeFolders[elementBelow.id]
        }

        // change old folder
        let objects = this.getProperticeByObjectsList()
        oldFolder.objects = objects.newRecordList
        oldFolder.folders = objects.newFolderList
        oldFolder.info.children = objects.newChildren

        // change new folder
        if (this.DADObject.typeObject==='record') {
            newFolder.objects.push('n'+this.DADObject.object.id)
        } else if (this.DADObject.typeObject==='folder') {
            newFolder.folders.push('f'+this.DADObject.object.id)
        }
        let newChildren = newFolder.folders.join(',') + ',' + newFolder.objects.join(',')
        if (newFolder.objects.length===0) newChildren=newChildren.slice(0,-1)
        newFolder.info.children = newChildren

        // необходимо для нормальной работы pathlist
        if (session.section === 'notes' && this.DADObject.typeObject === 'record') {
            content.notes[this.DADObject.object.id].parent_id = elementBelow.id
        } else if (session.section === 'notes' && this.DADObject.typeObject === 'folder') {
            content.noteFolders[this.DADObject.object.id].info.parent_id = elementBelow.id
        } else if (session.section === 'notices' && this.DADObject.typeObject === 'record') {
            content.notices[this.DADObject.object.id].parent_id = elementBelow.id
        } else if (session.section === 'notices' && this.DADObject.typeObject === 'folder') {
            content.noticeFolders[this.DADObject.object.id].info.parent_id = elementBelow.id
        } else {
            console.log("Error: parent_id hasn't changed")
        }

        // выполняем ajax для перемещения объекта в папку
        // Определяем тип объекта для API с учетом секции
        let objectType = ''
        if (this.DADObject.typeObject === DADSettings.recordClass) {
            objectType = session.section === 'notes' ? 'record' : 'notice'
        } else if (this.DADObject.typeObject === DADSettings.folderClass) {
            objectType = session.section === 'notes' ? 'recordFolder' : 'noticeFolder'
        }

        let data = {
            type: objectType,
            object_id: parseInt(this.DADObject.object.id),
            old_folder_id: parseInt(viewContent.currentFolderId),
            new_folder_id: parseInt(elementBelow.id),
        }

        const url = conf.Domains['server'] + conf.Urls.moveInside
        const options = {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            credentials: 'include',
            body: JSON.stringify(data),
        }
        const response = await conf.AJAX.send(url, options)

        if (response === undefined) {
            console.log(`Error: неопознанная ошибка при перемещении объекта в папку`)
            return
        }
        
        if (response.success) {
            console.log('Объект успешно перемещен в папку')
        } else {
            console.log(`Error: ${response.msg || 'Ошибка при перемещении объекта в папку'}`)
        }
        
    },
    run: function() {
        // Drag And Drop (DAD) events
        let objectsList = document.getElementById('objectsList')
        objectsList.addEventListener(`pointerdown`, this.pointerDownEvent.bind(this));
        document.addEventListener(`contextmenu`, this.disableRightButton.bind(this)); // disable right btn during DD
        // document.addEventListener(`pointerup`, change4th5thBTN);
        document.addEventListener(`pointermove`, this.pointerMoveEvent.bind(this));  // document, чтобы DADObject скользил вдоль границы DADArea, когда курсор ее покидает  
        document.addEventListener(`pointermove`, this.pointerMoveEventOut.bind(this));  // document, чтобы снятие выделение предыдущего объекта работало корректно
        document.addEventListener(`pointerup`, this.pointerUpEvent.bind(this));
        document.addEventListener(`keyup`, this.resetDADEvent.bind(this));
    }
}
DragAndDrop.run()

let mobileSettings = {
    timeout: 500, // press time for DAD start
    device: null, // mobile or desktop
    DAD: false,  // DAD work sensor
    holdDown: false,  // press touch for DAD start
    scrollId: null,  // setInterval ID
    scrollStep: 4,  // scroll offset (speed)

    getDeviceType: function() {  // getting type of a user device (mibile or desktop)
        // https://sky.pro/media/kak-opredelit-tip-ustrojstva-polzovatelya-s-pomoshhyu-javascript/
        let userAgent = navigator.userAgent.toLowerCase();
        let isMobile = /mobile|iphone|ipad|ipod|android|blackberry|mini|windows\sce|palm/i.test(userAgent);
    
        if (isMobile) {
        return "mobile";
        } else {
        return "desktop";
        }
    },
    setMobileDADAreaHeight: function() {  // set height of drag-area
        let heightScreen = window.screen.height
        let objectsList = document.getElementById('objectsList')
        let objectsList_y = objectsList.getBoundingClientRect().y
        objectsList.style['max-height'] = heightScreen-objectsList_y-50 + 'px'
        // 50px - footer height
    },
    pointerDownEvent: function(event) {  // DAD prepare by pointerdown
        event.preventDefault()
        this.holdDown = true
        setTimeout(this.DADStart.bind(this), this.timeout, event) // press 500ms
    },
    DADStart: function(event) {  // launch DAD in 0.5s
        if (!this.holdDown) return  // may be turn off in move and up events
        this.holdDown = false
        this.DAD = true
        DragAndDrop.pointerDownEvent(event) // usual DAD
    },
    pointerMoveEvent: function(event) {  // reset options
        this.holdDown = false

        // pointermove event doesn't disable touchmove
        // if (this.DAD) event.preventDefault()
    },
    pointerUpEvent: function(event) {  // reset options
        this.holdDown = false
        this.DAD = false
    },
    contexmenuEvent: function(event) {  // contexmenu works disabled
        if (event.pointerType === 'mouse') return  // mouse contexmenu works 
        event.preventDefault()
    },
    disableTouch: function(event) { // disable touch-action during DAD
        if (this.DAD) event.preventDefault()
    },
    DADScrolling: function(event) { // scrolling on the edges of the DAD-area
        // https://learn.javascript.ru/size-and-scroll-window
        let ratio = event.clientY/document.documentElement.clientHeight
        if (!DragAndDrop.DADObject.object) return
        if (!this.scrollId&&ratio<0.1) {
            this.scrollId = setInterval(() => window.scrollBy({top:-4, left: 0, behavior: "instant"}), 10)
        } else if (!this.scrollId&&ratio>0.9) {
            this.scrollId = setInterval(() => window.scrollBy({top:4, left: 0, behavior: "instant"}), 10)
        } else if (this.scrollId&&ratio>0.1&&ratio<0.9) {
            clearInterval(this.scrollId)
            this.scrollId = null
        }
    },
    run: function() {
        this.device = this.getDeviceType()
        if (this.device != 'mobile') return

        let objectsList = document.getElementById('objectsList')
        objectsList.addEventListener('pointerdown', this.pointerDownEvent.bind(this))
        document.addEventListener('pointermove', this.pointerMoveEvent.bind(this))
        document.addEventListener('pointerup', this.pointerUpEvent.bind(this))
        document.addEventListener('contextmenu', this.contexmenuEvent.bind(this))
        document.addEventListener('touchmove', this.disableTouch.bind(this), {passive: false})
        document.addEventListener('pointermove', this.DADScrolling.bind(this))
    }
}
mobileSettings.run()

const settingsGear = {
    ddArea: document.getElementById('objectsList'),
    gearMenu: document.getElementById('gearContextMenu'),
    elId: null,
    elType: null,
    offTimer: null,
    timerValue: 5000,  // time of disappearance, ms

    displayGearMenu: function(event) {  // display element-gear menu 
        let gear = event.target.closest('.content-svg')
        if (!(gear)) return
        
        event.preventDefault()
        let elemObj = gear.closest('.dd-object')

        this.gearMenu.style.display = 'block'
        this.gearMenu.style.left = event.pageX + 'px'
        this.gearMenu.style.top = event.pageY + 'px'
        
        this.elId = elemObj.id
        this.elType = elemObj.classList.contains('folder')?'folder':'record'

        clearTimeout(this.offTimer)
        this.offTimer = setTimeout(this.hideGearMenu.bind(this), this.timerValue)
    },
    hideGearMenu: function(event) {  // hide element-gear menu
        if (event) {
            let menu = event.target.closest('.gear-context-menu')
            if (menu) return
        }
        
        this.gearMenu.style.display = ''
        this.elId = null
        this.elType = null
    },
    changeEvent: function(event) {  // change event of the menu btn (open modal using edit mode)
        if (session.section == 'notes') modals.openEditModal(this.elType, this.elId)
        if (session.section == 'notices') modals.openEditNoticeModal(this.elType, this.elId)
        
        this.hideGearMenu()
    },
    delEvent: async function(event) {  // delete event of the menu btn (immediately using content.change.del***)
        const id = parseInt(this.elId)
        
        if (session.section === 'notes') {
            if (this.elType === 'record') {
                await content.change.delNote(id)
            } else {
                await content.change.delNoteFolder(id)
            }
        } else if (session.section === 'notices') {
            if (this.elType === 'record') {  // по историческим причинам в notices тоже record
                await content.change.delNotice(id)
            } else {
                await content.change.delNoticeFolder(id)
            }
        }
        
        this.hideGearMenu()
    },
    run: function() {
        this.ddArea.addEventListener('click', this.displayGearMenu.bind(this))
        this.ddArea.addEventListener('contextmenu', this.displayGearMenu.bind(this))

        const gearChange = document.getElementById('gearChange')
        const gearDel = document.getElementById('gearDel')
        gearChange.addEventListener('click', this.changeEvent.bind(this))
        gearDel.addEventListener('click', this.delEvent.bind(this))

        document.addEventListener('pointerdown', this.hideGearMenu.bind(this))
        document.addEventListener('keydown', this.hideGearMenu.bind(this))
    }
}
settingsGear.run()
