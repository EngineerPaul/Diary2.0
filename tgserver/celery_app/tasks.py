import asyncio
import logging
import uuid
from datetime import datetime

import aiohttp

from celery_app.celery_client import celery_app
from queries.to_server import send_mailing_list_report
from queries.to_tgbot import send_msg_bot
from services import RemindData
from utils.request_context import set_request_id

logger = logging.getLogger(__name__)


def _bind_task_request_id() -> str:
    """Функция для привязки request_id к задаче"""

    request_id = str(uuid.uuid4())
    set_request_id(request_id)
    return request_id


@celery_app.task  # beat
def celery_check_dispatch_date():
    """ Проверка даты отправки сообщений (10 сек) """
    _bind_task_request_id()
    try:
        dispatch_date = RemindData.get_date()
        if dispatch_date is None:
            logger.debug('No reminders scheduled for dispatch')
            return
        now = datetime.now()
        if now > dispatch_date:
            logger.info('Dispatch date reached, starting reminder delivery')
            send_all_reminders.delay()
        else:
            logger.debug(
                'Next dispatch in %s',
                dispatch_date - now.replace(microsecond=0),
            )
    finally:
        set_request_id(None)


@celery_app.task  # worker
def send_all_reminders():
    """ Отправка списка напоминаний воркером.
    Получение нового списка от сервера """
    _bind_task_request_id()
    try:
        rem_list = RemindData.get_reminders_list()
        if rem_list is None:
            logger.error('Reminder list is empty')
            return
        for rem in rem_list:
            asyncio.run(
                send_msg_bot(
                    chat_id=rem['chat_id'],
                    text=rem['text'],
                    user_id=rem['user_id'],
                    reminder_id=rem['reminder_id'],
                )
            )
        logger.info('Reminders sent', extra={'extra_fields': {'count': len(rem_list)}})
        RemindData.set_reminders_list(None)
        RemindData.set_date(None)

        async def _send_report():
            async with aiohttp.ClientSession() as session:
                await send_mailing_list_report(rem_list, session)

        asyncio.run(_send_report())
    finally:
        set_request_id(None)
