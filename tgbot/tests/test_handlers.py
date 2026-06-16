from datetime import datetime, timedelta
from unittest.mock import patch

import pytest

from tests.conftest import FakeBot, FakeCallbackQuery, FakeMessage

# импорт из handlers внутри тестов, чтобы правильно env в conftest установился правильно


@pytest.fixture
def bot():
    return FakeBot()


def test_start_registration_success(bot):
    from api.bot.handlers import start

    start(bot, command="start")

    msg = FakeMessage("/start 123", chat_id=11, from_user_id=22)

    with patch("api.bot.handlers.send_info", return_value=True) as send_info:
        bot.call_command("start", msg)

    # greeting + registration result
    assert len(bot.sent_messages) == 2
    assert bot.sent_messages[0]["chat_id"] == 11
    assert "Привет" in bot.sent_messages[0]["text"]
    assert bot.sent_messages[0]["parse_mode"] == "html"

    send_info.assert_called_once()
    payload = send_info.call_args.args[0]
    assert payload["user_id"] == "123"
    assert payload["tg_user_id"] == 22
    assert payload["tg_username"] == msg.from_user.username
    assert payload["chat_id"] == 11

    assert bot.sent_messages[1]["text"] == "Регистрация завершена"


def test_start_registration_failure(bot):
    from api.bot.handlers import start

    start(bot, command="start")
    msg = FakeMessage("/start 999", chat_id=11, from_user_id=22)

    with patch("api.bot.handlers.send_info", return_value=False):
        bot.call_command("start", msg)

    assert bot.sent_messages[-1]["text"].startswith("Ошибка при регистрации")


def test_sitelink_sends_html_link(bot):
    from api.bot.handlers import sitelink

    sitelink(bot, command="link")

    msg = FakeMessage("/link", chat_id=11, from_user_id=22)
    bot.call_command("link", msg)

    assert len(bot.sent_messages) == 1
    assert bot.sent_messages[0]["chat_id"] == 11
    assert "href" in bot.sent_messages[0]["text"]
    assert bot.sent_messages[0]["parse_mode"] == "html"


def test_create_reminder_flow_success(bot):
    from api.bot.handlers import create_reminder, create_reminder_title, create_reminder_date

    create_reminder(bot, command="create")

    # step 1: command -> ask title
    msg1 = FakeMessage("/create", chat_id=11, from_user_id=22)
    bot.call_command("create", msg1)
    assert "Укажите текст напоминания" in bot.sent_messages[-1]["text"]
    assert bot.next_step_handlers[-1][1] == create_reminder_title

    # step 2: user provides title -> ask date (now format comes from auth; patch it)
    msg2 = FakeMessage("My title", chat_id=11, from_user_id=22)
    with patch("api.bot.handlers.get_now_format", return_value="01.01.2030 12.00"):
        create_reminder_title(msg2, bot)
    assert "Укажите дату" in bot.sent_messages[-1]["text"]

    # step 3: user provides a valid date -> send_new_reminder -> success
    target_date = datetime.now() + timedelta(days=1)
    msg3 = FakeMessage("02.01.2030 12.00", chat_id=11, from_user_id=22)
    with (
        patch("api.bot.handlers.get_date", return_value={"status": True, "details": target_date}),
        patch("api.bot.handlers.send_new_reminder", return_value=True) as send_new,
    ):
        create_reminder_date(msg3, bot, "My title")

    send_new.assert_called_once()
    assert bot.sent_messages[-1]["text"] == "Напоминание успешно создано"


def test_create_reminder_date_invalid_repeats_step(bot):
    from api.bot.handlers import create_reminder_date

    msg = FakeMessage("bad date", chat_id=11, from_user_id=22)
    with patch("api.bot.handlers.normalize_reminder_date_input", return_value=None):
        create_reminder_date(msg, bot, "Title")

    assert bot.sent_messages[-1]["text"].startswith("Неверный формат даты")
    # next step handler should point back to create_reminder_date with original title
    _, fn, args = bot.next_step_handlers[-1]
    assert fn == create_reminder_date
    assert args == (bot, "Title")


def test_create_reminder_date_short_format(bot):
    from api.bot.handlers import create_reminder_date

    future = datetime.now() + timedelta(days=5)
    msg = FakeMessage(f"{future.day} 12:00", chat_id=11, from_user_id=22)
    with patch("api.bot.handlers.send_new_reminder", return_value=True) as send_new:
        create_reminder_date(msg, bot, "My title")

    send_new.assert_called_once()
    sent_date = send_new.call_args.args[2]
    assert sent_date.hour == 12
    assert sent_date.minute == 0
    assert bot.sent_messages[-1]["text"] == "Напоминание успешно создано"


def test_callback_repeat_hour_success(bot):
    from api.bot.handlers import callback

    callback(bot)

    cb = FakeCallbackQuery("rep_hour,10,1", chat_id=11)
    with patch("api.bot.handlers.send_notice_shift", return_value=True) as send_shift:
        bot.call_callback(cb)

    send_shift.assert_called_once_with(1, 10, "hour", 11)
    assert bot.sent_messages[-1]["text"] == "Напоминание перенесено на 1 час"


def test_callback_repeat_day_failure(bot):
    from api.bot.handlers import callback

    callback(bot)

    cb = FakeCallbackQuery("rep_day,10,1", chat_id=11)
    with patch("api.bot.handlers.send_notice_shift", return_value=False):
        bot.call_callback(cb)

    assert bot.sent_messages[-1]["text"] == "Ошибка изменения напоминания"

