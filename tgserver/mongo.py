from typing import List, Dict
from config import MY_TG_ID


upcoming_reminders: List[Dict] = []
upcoming_date = 'now'

upcoming_reminders.append(
    {
        'user_id': 100,
        'reminder_id': 100,
        'message': 'Тестовое напоминание',
        'tg_id': MY_TG_ID,
    }
)
