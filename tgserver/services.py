from typing import List, Dict
from datetime import datetime, timedelta
import json

from config import MY_TG_ID
from redis_client import redis_set, redis_get


class RemindData():
    """ Cls for interaction with dispatch date and reminders list """

    def get_date() -> datetime:
        """ getting date from the redis """

        iso_date = redis_get('date')
        if iso_date:
            date = datetime.fromisoformat(iso_date)
            return date
        else:
            return None

    def get_reminders_list() -> List:
        """ gettings reminders list from the redis """

        json_rem_list = redis_get('reminders_list')
        if json_rem_list:
            rem_list = json.loads(json_rem_list)
            return rem_list
        else:
            return None

    def set_date(date: datetime | None):
        """ saving date in the redis """

        if date is None:
            redis_set('date', None)
        else:
            iso_date = date.isoformat()
            redis_set('date', iso_date)

    def set_reminders_list(rem_list: List[Dict] | None):
        """ saving reminders list in the redis """

        if rem_list is None:
            redis_set('reminders_list', None)
        else:
            json_rem_list = json.dumps(rem_list)
            redis_set('reminders_list', json_rem_list)


RemindData.set_reminders_list(None)  # default
RemindData.set_date(None)  # default
