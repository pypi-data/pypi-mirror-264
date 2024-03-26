import pytz
import requests

from datetime import datetime

from .settings import BACKEND_APP_CRASH_ALERTS_URL


def alert(api_key: str, datetime: datetime, log: str, tag: str | None):

    try:
        response = requests.post(
            BACKEND_APP_CRASH_ALERTS_URL,
            data={
                'datetime': datetime,
                'log': log,
                'tag': tag
            },
            headers={ 'X-API-KEY': api_key }
        )

        if response.status_code == 200:
            pass
        else:
            pass
    except requests.exceptions.RequestException as e:
        raise e


class Guardog:

    def __init__(self, api_key: str, uid: str, service_id: str):

        self.api_key = api_key
        self.uid = uid
        self.service_id = service_id

    def watch(self, tag):

        def inner(func):
            def wrapper(*args, **kwargs):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    dt = datetime.utcnow()
                    dt = dt.replace(tzinfo=pytz.utc)
                    alert(
                        api_key=self.api_key,
                        datetime=dt,
                        log=e,
                        tag=tag
                    )
                    raise
            return wrapper

        return inner
