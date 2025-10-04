from handlers import (
    start,
    sitelink, create_reminder,
    callback,

    get_info, send_test,
)

from config import DEBUG


def command_registry(bot):
    start(bot, command='start')
    sitelink(bot, command='link')
    create_reminder(bot, command='create')

    callback(bot)

    if DEBUG:
        get_info(bot, command='info')
        send_test(bot, command='send')
