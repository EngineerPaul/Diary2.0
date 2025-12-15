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

let ajax = {
    authId: null, // id for authenticate
    recordId: null, // id of whole record

    getAuthId: function() {
        return '1234'
    },
    getRecordId: function() {
        return 19
    },
    getRecordInfo: function() { // getting theme, creationDate, settings
        let blankContent = {
            theme: 'Theme',
            creationDate: '25.04.2025 5:40',
            settings: {},
        }
    },
    getNotes: function() { // getting notes list by record id by date
        let blankContent = [ // like [[id, creationDate, content], ...]
            [2, 'Комарницкий Павел', '2025-05-01T06:30:00.243Z', 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Proin in semper nisi. Morbi eu purus sed nibh blandit maximus vel ac orci. Integer auctor est et lorem dapibus dapibus. Praesent sollicitudin mauris in metus facilisis, eu facilisis mauris congue. Curabitur molestie sem ligula, id interdum leo euismod nec. Suspendisse ullamcorper diam eros, non aliquam libero porta non. Fusce gravida auctor quam, quis volutpat libero aliquet id. Praesent lobortis risus vitae velit sodales maximus. Vivamus mollis sed tortor sit amet pretium. Duis aliquam enim eleifend purus mollis pharetra. Praesent nibh massa, viverra iaculis imperdiet id, aliquet vitae augue. In dapibus, felis vitae volutpat aliquet, ex lacus efficitur odio, a venenatis nulla arcu et est. Suspendisse placerat nisl quis nisi iaculis, sit amet accumsan erat venenatis. Quisque lorem lorem, porttitor eget scelerisque in, vulputate in orci. Vivamus maximus volutpat velit, nec tincidunt tellus posuere faucibus.'],
            [4, 'Комарницкий Павел', '2025-05-01T06:35:00.243Z', 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Proin in semper nisi. Morbi eu purus sed nibh blandit maximus vel ac orci. Integer auctor est et lorem dapibus dapibus. Praesent sollicitudin mauris in metus facilisis, eu facilisis mauris congue. Curabitur molestie sem ligula, id interdum leo euismod nec. Suspendisse ullamcorper diam eros, non aliquam libero porta non. Fusce gravida auctor quam, quis volutpat libero aliquet id. Praesent lobortis risus vitae velit sodales maximus. Vivamus mollis sed tortor sit amet pretium. Duis aliquam enim eleifend purus mollis pharetra. Praesent nibh massa, viverra iaculis imperdiet id, aliquet vitae augue. In dapibus, felis vitae volutpat aliquet, ex lacus efficitur odio, a venenatis nulla arcu et est. Suspendisse placerat nisl quis nisi iaculis, sit amet accumsan erat venenatis. Quisque lorem lorem, porttitor eget scelerisque in, vulputate in orci. Vivamus maximus volutpat velit, nec tincidunt tellus posuere faucibus.'],
            [6, 'Комарницкий Павел', '2025-05-01T06:40:00.243Z', 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Proin in semper nisi. Morbi eu purus sed nibh blandit maximus vel ac orci. Integer auctor est et lorem dapibus dapibus. Praesent sollicitudin mauris in metus facilisis, eu facilisis mauris congue. Curabitur molestie sem ligula, id interdum leo euismod nec. Suspendisse ullamcorper diam eros, non aliquam libero porta non. Fusce gravida auctor quam, quis volutpat libero aliquet id. Praesent lobortis risus vitae velit sodales maximus. Vivamus mollis sed tortor sit amet pretium. Duis aliquam enim eleifend purus mollis pharetra. Praesent nibh massa, viverra iaculis imperdiet id, aliquet vitae augue. In dapibus, felis vitae volutpat aliquet, ex lacus efficitur odio, a venenatis nulla arcu et est. Suspendisse placerat nisl quis nisi iaculis, sit amet accumsan erat venenatis. Quisque lorem lorem, porttitor eget scelerisque in, vulputate in orci. Vivamus maximus volutpat velit, nec tincidunt tellus posuere faucibus.'],
            [8, 'Комарницкий Павел', '2025-05-01T06:45:00.243Z', 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Proin in semper nisi. Morbi eu purus sed nibh blandit maximus vel ac orci. Integer auctor est et lorem dapibus dapibus. Praesent sollicitudin mauris in metus facilisis, eu facilisis mauris congue. Curabitur molestie sem ligula, id interdum leo euismod nec. Suspendisse ullamcorper diam eros, non aliquam libero porta non. Fusce gravida auctor quam, quis volutpat libero aliquet id. Praesent lobortis risus vitae velit sodales maximus. Vivamus mollis sed tortor sit amet pretium. Duis aliquam enim eleifend purus mollis pharetra. Praesent nibh massa, viverra iaculis imperdiet id, aliquet vitae augue. In dapibus, felis vitae volutpat aliquet, ex lacus efficitur odio, a venenatis nulla arcu et est. Suspendisse placerat nisl quis nisi iaculis, sit amet accumsan erat venenatis. Quisque lorem lorem, porttitor eget scelerisque in, vulputate in orci. Vivamus maximus volutpat velit, nec tincidunt tellus posuere faucibus.'],
            [11, 'Комарницкий Павел', '2025-05-01T06:50:00.243Z', 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Proin in semper nisi. Morbi eu purus sed nibh blandit maximus vel ac orci. Integer auctor est et lorem dapibus dapibus. Praesent sollicitudin mauris in metus facilisis, eu facilisis mauris congue. Curabitur molestie sem ligula, id interdum leo euismod nec. Suspendisse ullamcorper diam eros, non aliquam libero porta non. Fusce gravida auctor quam, quis volutpat libero aliquet id. Praesent lobortis risus vitae velit sodales maximus. Vivamus mollis sed tortor sit amet pretium. Duis aliquam enim eleifend purus mollis pharetra. Praesent nibh massa, viverra iaculis imperdiet id, aliquet vitae augue. In dapibus, felis vitae volutpat aliquet, ex lacus efficitur odio, a venenatis nulla arcu et est. Suspendisse placerat nisl quis nisi iaculis, sit amet accumsan erat venenatis. Quisque lorem lorem, porttitor eget scelerisque in, vulputate in orci. Vivamus maximus volutpat velit, nec tincidunt tellus posuere faucibus.'],
        ]
        return blankContent
    },
    getImages: function() { // getting images list by record id by date
        // everything needs to be rewritten
        let blankImages = [ // like [[groupId, creationDate, [[imgId, src], ...]], ...]
            [
                7, 'Комарницкий Павел', '2025-05-01T06:33:00.243Z', [
                    [1, "/static/img/forTest/1.jpg"], 
                    [2, "/static/img/forTest/2.jpg"], 
                    [3, "/static/img/forTest/3.jpg"], 
                    [4, "/static/img/forTest/4.jpg"], 
                    [5, "/static/img/forTest/5.jpg"], 
                    [6, "/static/img/forTest/6.jpg"], 
                ],
            ],
            [
                9, 'Комарницкий Павел', '2025-05-01T06:48:00.243Z', [
                    [7, "/static/img/forTest/1.jpg"], 
                    [8, "/static/img/forTest/2.jpg"], 
                    [9, "/static/img/forTest/3.jpg"], 
                    [10, "/static/img/forTest/4.jpg"], 
                    [11, "/static/img/forTest/5.jpg"], 
                    [12, "/static/img/forTest/6.jpg"], 
                ],
            ]
        ]
        return blankImages
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

        return response
    },

    // blanks
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
    run: function() {
        this.authId = this.getAuthId()
        this.recordId = this.getRecordId()
    }
}
ajax.run()
ajax.getContent()

let content = {
    theme: null, // title of whole record
    content: [], // all content ids like [{type, id}, ...] by date. Type is note or imagesGroup
    notes: {}, // notes objs like {id: this.Note, ...}
    images: {}, // images objs like {id: this.Image, ...}
    imagesGroups: {}, // images groups like {groupId: this.ImagesGroup, ...}

    Note: function(noteId, author, date, content) { // create note object using
        this.id = noteId //num
        this.author = author
        this.date = new Date(date) //str
        this.content = content //str
    },
    Image: function(imageId, path) { // create image object using
        this.id = imageId
        this.path = path
    },
    ImagesGroup: function(imagesGroupId, author, date, images) { // create images group like Note
        this.id = imagesGroupId //num
        this.author = author
        this.date = new Date(date) //str
        this.content = images //list of numeric ids
    },
    getContent: function() { // getting notes, images, images groups and content using ajax
        let rawNotes = ajax.getNotes()
        for (let i=0; i<rawNotes.length; i++) {
            this.notes[rawNotes[i][0]] = new this.Note(...rawNotes[i])
        }

        let rawImages = ajax.getImages()
        for (let igi=0; igi<rawImages.length; igi++) {
            let idList = []
            for (let i=0; i<rawImages[igi][3].length; i++) {
                this.images[rawImages[igi][3][i][0]] = new this.Image(...rawImages[igi][3][i])
                idList.push(rawImages[igi][3][i][0])
            }
            this.imagesGroups[rawImages[igi][0]] = new this.ImagesGroup(
                rawImages[igi][0], rawImages[igi][1], rawImages[igi][2], idList)
        }
        
        let noteKeys = Object.keys(this.notes)
        let imagesGroupsKeys = Object.keys(this.imagesGroups)
        let ni = 0 
        let igi = 0
        for (let i=0; i<Object.keys(this.notes).length+Object.keys(this.imagesGroups).length; i++) {

            let noteKey = noteKeys[ni]?
                noteKeys[ni]:
                null
            let groupKey = imagesGroupsKeys[igi]?
                imagesGroupsKeys[igi]:
                null

            if (this.notes[noteKey] && this.imagesGroups[groupKey]) {
                if (this.notes[noteKey].date.getTime() < this.imagesGroups[groupKey].date.getTime()) {
                    this.content.push({'type': 'note', 'id': this.notes[noteKey].id})
                    ni += 1
                } else {
                    this.content.push({'type': 'imagesGroup', 'id': this.imagesGroups[groupKey].id})
                    igi += 1
                }
            } else {
                if (this.notes[noteKey]) {
                    this.content.push({'type': 'note', 'id': this.notes[noteKey].id})
                    ni += 1
                } else if (this.imagesGroups[groupKey]) {
                    this.content.push({'type': 'imagesGroup', 'id': this.imagesGroups[groupKey].id})
                    igi += 1
                } else {
                    console.log('Error: the both doesnt exist')
                }
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
    viewContent: function() { // display all content using all properties
        let content = document.getElementById('content')
        content.innerHTML = ''
        for (let i=0; i<this.content.length; i++) {
            if (this.content[i].type === 'note') {
                this.viewNote(this.content[i].id)
            } else if (this.content[i].type === 'imagesGroup') {
                this.viewImages(this.content[i].id)
            } else {
                console.log('Error: content type is incorrect')
            }
        }
    },
    viewNote: function(noteId) { // display a note block
        let content = document.getElementById('content')
        let record = this.createElement({
            tag: 'div',
            classList: ['record'],
            parent: content,
            params: {id: noteId},
        })
        let recordHeader = this.createElement({
            tag: 'div',
            classList: ['record-header'],
            parent: record,
            params: {},
        })
        let date = this.createElement({
            tag: 'div',
            classList: ['date'],
            parent: recordHeader,
            params: {textContent: this.notes[noteId].date},
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
            params: {textContent: this.notes[noteId].content},
        })
    },
    viewImages: function(groupId) { // display an images block
        let content = document.getElementById('content')
        let images = this.createElement({
            tag: 'div',
            classList: ['images'],
            parent: content,
            params: {id: groupId},
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
        let imageArea = this.createElement({
            tag: 'div',
            classList: ['image-area'],
            parent: slider,
            params: {},
        })
        let imagesList = this.imagesGroups[groupId].content
        let loadedImagesCount = 0
        let totalImagesCount = imagesList.length
        
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
                params: {src: this.images[imagesList[i]].path, id: imagesList[i]},
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
                    // Все изображения загружены, пересчитываем высоту блока
                    this.updateSliderHeight(slider)
                }
            })
            
            // Если изображение уже загружено (из кэша), сразу увеличиваем счетчик
            if (img.complete) {
                loadedImagesCount++
                if (loadedImagesCount === totalImagesCount) {
                    this.updateSliderHeight(slider)
                }
            }
        }
        let editor = this.createSVG({
            parent: images,
            className: 'editor',
            viewBox: '0 0 512.021 512.021',
            pathLst: ['M301.258,256.01L502.645,54.645c12.501-12.501,12.501-32.769,0-45.269c-12.501-12.501-32.769-12.501-45.269,0l0,0   L256.01,210.762L54.645,9.376c-12.501-12.501-32.769-12.501-45.269,0s-12.501,32.769,0,45.269L210.762,256.01L9.376,457.376   c-12.501,12.501-12.501,32.769,0,45.269s32.769,12.501,45.269,0L256.01,301.258l201.365,201.387   c12.501,12.501,32.769,12.501,45.269,0c12.501-12.501,12.501-32.769,0-45.269L301.258,256.01z'],
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
    run: function() {
        this.getContent()
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

