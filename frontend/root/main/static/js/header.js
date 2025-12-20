const headerSections = {  // main section handler
    homeUrl: '/',  // homepage URL

    initHeaderState: function() {  // set the initial state when the page loads
        const noteSection = document.getElementById('noteSection')
        const noticeSection = document.getElementById('noticeSection')
        
        if (!noteSection || !noticeSection) return
        
        const isHomePage = document.getElementById('objectsList') !== null
        
        if (isHomePage) {
            const currentSection = sessionStorage.getItem('section') || 'notes'
            const sectionId = currentSection === 'notes' ? 'noteSection' : 'noticeSection'
            const sectionEl = document.getElementById(sectionId)
            const sectionSecond = currentSection === 'notes' ? noticeSection : noteSection
            
            if (sectionEl && sectionSecond) { // exist check
                noteSection.classList.remove('selected')
                noticeSection.classList.remove('selected')
                sectionEl.classList.add('selected')
            }
        } else {
            noteSection.classList.remove('selected')
            noticeSection.classList.remove('selected')
        }
    },

    handleSectionClick: function(event) {  // section click event handler
        const sec = event.target.closest('.header-field')
        if (!sec) return  // exist check

        const sectionMapping = {
            'noteSection': 'notes',
            'noticeSection': 'notices'
        }
        const sectionName = sectionMapping[sec.id]
        if (!sectionName) return  // exist check

        const currentSection = sessionStorage.getItem('section')
        const isHomePage = document.getElementById('objectsList') !== null
        
        if (!isHomePage) { // open homepage
            sessionStorage.setItem('section', sectionName)
            window.location.href = this.homeUrl
            return
        }

        if (currentSection === sectionName) return

        sessionStorage.setItem('section', sectionName)

        const sectionEl = document.getElementById(sec.id)
        const sectionSecondId = sectionName === 'notes' ? 'noticeSection' : 'noteSection'
        const sectionSecond = document.getElementById(sectionSecondId)
        
        if (sectionEl && sectionSecond) {
            sectionEl.classList.add('selected')
            sectionSecond.classList.remove('selected')
        }

        // gen custom event for updating content
        const sectionChangeEvent = new CustomEvent('sectionChanged', {
            detail: { section: sectionName }
        })
        document.dispatchEvent(sectionChangeEvent)
    },

    run: function() {
        const sections = document.getElementById('sections')
        if (!sections) return
        
        sections.addEventListener('click', this.handleSectionClick.bind(this))
        
        this.initHeaderState()
    }
}
headerSections.run()

