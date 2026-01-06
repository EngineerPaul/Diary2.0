export const createElement = function(options) { // create usual HTML elem
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
}

export const createSVG = function(options) { // create usual HTML svg elem
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
}

