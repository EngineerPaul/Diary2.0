from telebot import types


def get_markup(user_id, reminder_id):
    markup = types.InlineKeyboardMarkup()

    data = f'rep_hour,{reminder_id},{user_id}'
    btn_repeat_hour = types.InlineKeyboardButton(
        text='Перенести на час',
        callback_data=data
    )

    data = f'rep_day,{reminder_id},{user_id}'
    btn_repeat_day = types.InlineKeyboardButton(
        text='Перенести на день',
        callback_data=data
    )
    markup.add(btn_repeat_hour, btn_repeat_day)

    return markup
