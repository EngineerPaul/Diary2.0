export const slider = {
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

export const sliderView = {
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
    viewImages: function(imagesData, domUtils) { // display an images block from messages data
        let content = document.getElementById('content')
        let images = domUtils.createElement({
            tag: 'div',
            classList: ['images'],
            parent: content,
            params: {id: imagesData.msg_id},
        })

        let sliderDirecrionLeft = domUtils.createElement({
            tag: 'div',
            classList: ['slide-direction'],
            parent: images,
            params: {},
        })
        let rectangleLeft = domUtils.createElement({
            tag: 'div',
            classList: ['rectangle'],
            parent: sliderDirecrionLeft,
            params: {},
        })
        rectangleLeft['dataset']['direction'] = 'left'
        let svgLeft = domUtils.createSVG({
            parent: rectangleLeft,
            className: '',
            viewBox: '0 0 24 24',
            pathLst: ['M17.921,1.505a1.5,1.5,0,0,1-.44,1.06L9.809,10.237a2.5,2.5,0,0,0,0,3.536l7.662,7.662a1.5,1.5,0,0,1-2.121,2.121L7.688,15.9a5.506,5.506,0,0,1,0-7.779L15.36.444a1.5,1.5,0,0,1,2.561,1.061Z'],
        })

        let slider = domUtils.createElement({
            tag: 'div',
            classList: ['slider'],
            parent: images,
            params: {},
        })
        // Скрываем блок до загрузки всех изображений
        slider.style.opacity = '0'
        let imageArea = domUtils.createElement({
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
            let image = domUtils.createElement({
                tag: 'div',
                classList: ['image'],
                parent: imageArea,
                params: {},
            })
            let img = domUtils.createElement({
                tag: 'img',
                classList: [],
                parent: image,
                params: {src: imagesList[i].url, id: imagesList[i].image_id},
            })
            let imageCross = domUtils.createSVG({
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
        let editor = domUtils.createSVG({
            parent: images,
            className: 'editor',
            viewBox: '0 0 24 24',
            pathLst: [
                'M1.172,19.119A4,4,0,0,0,0,21.947V24H2.053a4,4,0,0,0,2.828-1.172L18.224,9.485,14.515,5.776Z',
                'M23.145.855a2.622,2.622,0,0,0-3.71,0L15.929,4.362l3.709,3.709,3.507-3.506A2.622,2.622,0,0,0,23.145.855Z'
            ],
        })
        let cross = domUtils.createSVG({
            parent: images,
            className: 'cross',
            viewBox: '0 0 512.021 512.021',
            pathLst: ['M301.258,256.01L502.645,54.645c12.501-12.501,12.501-32.769,0-45.269c-12.501-12.501-32.769-12.501-45.269,0l0,0   L256.01,210.762L54.645,9.376c-12.501-12.501-32.769-12.501-45.269,0s-12.501,32.769,0,45.269L210.762,256.01L9.376,457.376   c-12.501,12.501-12.501,32.769,0,45.269s32.769,12.501,45.269,0L256.01,301.258l201.365,201.387   c12.501,12.501,32.769,12.501,45.269,0c12.501-12.501,12.501-32.769,0-45.269L301.258,256.01z'],
        })
        let sliderDirecrionRight = domUtils.createElement({
            tag: 'div',
            classList: ['slide-direction'],
            parent: images,
            params: {},
        })
        let rectangleRight = domUtils.createElement({
            tag: 'div',
            classList: ['rectangle'],
            parent: sliderDirecrionRight,
            params: {},
        })
        rectangleRight.dataset['direction'] = 'right'
        let svgRight = domUtils.createSVG({
            parent: rectangleRight,
            className: '',
            viewBox: '0 0 24 24',
            pathLst: ['M6.079,22.5a1.5,1.5,0,0,1,.44-1.06l7.672-7.672a2.5,2.5,0,0,0,0-3.536L6.529,2.565A1.5,1.5,0,0,1,8.65.444l7.662,7.661a5.506,5.506,0,0,1,0,7.779L8.64,23.556A1.5,1.5,0,0,1,6.079,22.5Z'],
        })
    },
    delImage: function(imageId, msgId, messages) { // update local state for deletion any single image
        const imageIdNum = Number(imageId)
        const msgIdNum = Number(msgId)
        
        let imagesGroup = null
        let groupIndex = -1
        for (let i = 0; i < messages.length; i++) {
            if (messages[i].type === 'images' && messages[i].msg_id === msgIdNum) {
                imagesGroup = messages[i]
                groupIndex = i
                break
            }
        }
        
        if (!imagesGroup || !imagesGroup.images) {
            console.log('Error: группа изображений не найдена')
            return false
        }
        
        const imageIndex = imagesGroup.images.findIndex(img => img.image_id === imageIdNum)
        if (imageIndex !== -1) {
            imagesGroup.images.splice(imageIndex, 1)
        }

        if (imagesGroup.images.length === 0 && groupIndex !== -1) {
            messages.splice(groupIndex, 1)
        }
        
        return true
    },
    delImages: function(msgId, messages) { // update local state for deletion any image group (with images)
        const msgIdNum = Number(msgId)
        const initialLength = messages.length
        for (let i = messages.length - 1; i >= 0; i--) {
            if (messages[i].type === 'images' && messages[i].msg_id === msgIdNum) {
                messages.splice(i, 1)
                break
            }
        }
        return messages.length < initialLength
    }
}

