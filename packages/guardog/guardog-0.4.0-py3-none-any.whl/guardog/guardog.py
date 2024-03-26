import json
import pytz
import requests
import traceback

from datetime import datetime

from .settings import BACKEND_APP_CRASH_ALERTS_URL


def alert(uid: str, service_id: str, api_key: str, datetime: datetime, log: str, tag: str | None):

    try:
        response = requests.post(
            BACKEND_APP_CRASH_ALERTS_URL + f'/uid/{uid}/service-id/{service_id}/alert',
            data=json.dumps({
                'datetime': datetime.isoformat(),
                'log': log,
                'tag': tag
            }),
            headers={
                'X-API-KEY': api_key,
                'content-type': "application/json"
            }
        )

        if response.status_code == 200:
            pass
        else:
            raise requests.exceptions.RequestException(response.status_code, response.text)
    except requests.exceptions.RequestException as e:
        raise e


class Guardog:

    def __init__(self, api_key: str, uid: str, service_id: str):

        self.api_key = api_key
        self.uid = uid
        self.service_id = service_id

    def watch(self, tag=None):

        def inner(func):
            def wrapper(*args, **kwargs):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    dt = datetime.utcnow()
                    dt = dt.replace(tzinfo=pytz.utc)
                    alert(
                        uid=self.uid,
                        service_id=self.service_id,
                        api_key=self.api_key,
                        datetime=dt,
                        log=traceback.format_exc(),
                        tag=tag
                    )
                    # raise
            return wrapper

        return inner

    def alert(self, error_log: str, tag: str = None):

        dt = datetime.utcnow()
        dt = dt.replace(tzinfo=pytz.utc)
        alert(
            uid=self.uid,
            service_id=self.service_id,
            api_key=self.api_key,
            datetime=dt,
            log=error_log,
            tag=tag
        )
