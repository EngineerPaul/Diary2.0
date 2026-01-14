import { Domains, Urls, AJAX, TelegramBot } from "./conf.js"

function loadUserProfile() {
    try {
        const userInfo = localStorage.getItem('userInfo');
        
        if (userInfo) {
            const user = JSON.parse(userInfo);
            
            // Отображаем логин
            const usernameElement = document.getElementById('username');
            if (usernameElement) {
                usernameElement.textContent = user.username || '-';
            }
            
            // Отображаем TG никнейм
            const tgNicknameElement = document.getElementById('tgNickname');
            const enableBotSection = document.getElementById('enableBotSection');
            
            if (tgNicknameElement && enableBotSection) {
                if (user.tg_nickname && user.tg_nickname.trim() !== '') {
                    tgNicknameElement.textContent = user.tg_nickname;
                    enableBotSection.style.display = 'none';
                } else {
                    tgNicknameElement.textContent = 'Не указан';
                    enableBotSection.style.display = 'block';
                }
            }
        } else {
            // Если информации о пользователе нет в localStorage
            console.warn('User information not found in localStorage');
            const usernameElement = document.getElementById('username');
            const tgNicknameElement = document.getElementById('tgNickname');
            const enableBotSection = document.getElementById('enableBotSection');
            
            if (usernameElement) usernameElement.textContent = '-';
            if (tgNicknameElement) tgNicknameElement.textContent = '-';
            if (enableBotSection) enableBotSection.style.display = 'block';
        }
    } catch (error) {
        console.error('Error loading user profile:', error);
    }
}

function botActivation() {
    const userInfo = JSON.parse(localStorage.getItem('userInfo'));
    
    if (!userInfo || !userInfo.id) {
        console.error('User information not found');
        alert('Ошибка: информация о пользователе не найдена');
        return;
    }

    const url = Domains['auth'] + Urls['tgAuthDate'];
    const options = {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        credentials: 'include',
        body: JSON.stringify({
            user_id: userInfo.id
        })
    };

    AJAX.send(url, options)
        .then(response => {
            if (response && response.success) {
                // Генерируем ссылку для перехода к боту
                const botLink = `${TelegramBot.baseUrl}${TelegramBot.name}?start=${userInfo.id}`;
                
                // Осуществляем переход по ссылке
                window.location.href = botLink;
            } else {
                console.error('Server response error:', response);
                alert('Ошибка сервера при активации бота');
            }
        })
        .catch(error => {
            console.error('Error activating bot:', error);
            alert('Ошибка при активации бота. Попробуйте позже.');
        });
}

const botActivationBtn = document.getElementById('enableBotBtn')
botActivationBtn.addEventListener('click', botActivation)

document.addEventListener('DOMContentLoaded', loadUserProfile);
