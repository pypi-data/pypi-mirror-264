from time import time
from random import randint
from requests import Session
from msgspec import json as msgspec_json
from .lib.util import signature, gen_deviceId
from .lib.util.exceptions import CheckException

# add by August Light

api = "http://service.aminoapps.com:80/api/v1"
device_id = gen_deviceId()

class CustomSession(Session):
    def request(self, method, url, *args, **kwargs):

        headers = kwargs.setdefault("headers", {})

        if method.lower() == "post":
            if "data" in kwargs or "json" in kwargs:
                data = kwargs.get('data') or kwargs.get("json")
                
                data["timestamp"] = int(time() * 1000)

                if not isinstance(data, str):
                    try:
                        data = msgspec_json.encode(data)
                    except (TypeError, ValueError):
                        print("Error: data must be structure JSON")
                        return None

                headers["Content-Type"] = "application/json"
                headers["NDC-MSG-SIG"] = signature(data)

            else:
                headers["Content-Type"] = "application/x-www-form-urlencoded"
            
        headers["NDCDEVICEID"] = device_id
        headers["User-Agent"] = f"Apple iPhone{randint(0,99999)},1 iOS v16.5 Main/3.19.0"

        response = super().request(method, url, *args, **kwargs)

        if response.status_code != 200:
            CheckException(response.text)

        response.json = lambda: msgspec_json.decode(response.content)

        return response


def socket_required(func):
    def wrapper(self, *args, **kwargs):
        if not self.socket_enabled:
            raise Exception("Sockets are disabled, this method cannot be used.")
        return func(self, *args, **kwargs)
    return wrapper