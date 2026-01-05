import * as conf from "../conf.js";

export const noticeFormUtils = {  // utils for notice create/change forms
    viewPeriodic: function(event) { // getting user friendly periodic script
        const fNoticePeriodTotal = document.getElementById('fNoticePeriodTotal')
        let totalMessage = ''

        const fNoticeDay = document.getElementById('fNoticeDay').value
        const fNoticeWeek = document.getElementById('fNoticeWeek').value || '0'
        const fNoticeMonth = document.getElementById('fNoticeMonth').value || '0'
        const fNoticeYear = document.getElementById('fNoticeYear').value || '0'
        const period = `${fNoticeDay},${fNoticeWeek},${fNoticeMonth},${fNoticeYear}`

        if (!fNoticeDay) {
            fNoticePeriodTotal.textContent = 'Необходимо указать день'
            return
        }
        
        // дни
        if (/^\d+,0,0,0$/.test(period)) {
            totalMessage += `Каждые ${fNoticeDay} дней (дня)`
        } else if (/^\d+,\d+,\d+,\d+$/.test(period)) {
            totalMessage += `Каждый ${fNoticeDay}(ый) день`
        }

        // недели
        if (/^\d+,0,\d+,\d+$/.test(period)) {
            totalMessage += ``
        } else if (/^\d+,\d+,0,0$/.test(period)) {
            totalMessage += ` каждой ${fNoticeWeek}(ой) недели в месяце`
        } else if (/^\d+,\d+,\d+,0$/.test(period)) {
            totalMessage += ` каждой ${fNoticeWeek}(ой) недели в году`
        }

        // месяц
        if (/^\d+,\d+,0,\d+$/.test(period)) {
            totalMessage += ``
        } else if (/^\d+,\d+,\d+,0$/.test(period)) {
            totalMessage += ` каждого ${fNoticeMonth}(го) месяца`
        }

        // год
        if (/^\d+,\d+,\d+,0$/.test(period)) {
            totalMessage += ``
        } else if (/^\d+,\d+,\d+,\d+$/.test(period)) {
            totalMessage += ` каждые ${fNoticeYear} лет`
        }

        fNoticePeriodTotal.textContent = totalMessage
    },
    
    getNextDate: async function(event) { // getting next date by date, time and period
        const fNoticeNextDate = document.getElementById('fNoticeNextDate')
        fNoticeNextDate.textContent = ''

        const fNoticeDay = document.getElementById('fNoticeDay').value
        const fNoticeWeek = document.getElementById('fNoticeWeek').value || '0'
        const fNoticeMonth = document.getElementById('fNoticeMonth').value || '0'
        const fNoticeYear = document.getElementById('fNoticeYear').value || '0'
        const period = `${fNoticeDay},${fNoticeWeek},${fNoticeMonth},${fNoticeYear}`
        const date = document.getElementById('fNoticeInitialDate').value
        const time = document.getElementById('fNoticePeriodTime').value

        
        if (!(fNoticeDay && /^\d+,\d+,\d+,\d+$/.test(period) && date && time)) {
            return
        }
        const initialDateTime = new Date(`${date}T${time}`)
        const now = new Date()
        if (initialDateTime <= now) {
            fNoticeNextDate.textContent = 'Ошибка: указана прошедшая дата'
            return
        }
        
        const url = conf.Domains['server'] + conf.Urls['getNextDate']
        console.log(url)
        const data = {
            'period': period,
            'initial_date': date,
            'time': time,
        }

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
            console.log(`Error: неопознанная ошибка при получении следующей даты`)
            return
        }
        
        if (fNoticeNextDate) {
            if (response.success === false) {
                console.log(`Error: ${response.msg || 'Ошибка при получении следующей даты'}`)
                fNoticeNextDate.textContent = ''
            } else {
                fNoticeNextDate.textContent = response || ''
            }
        }
    }
}

