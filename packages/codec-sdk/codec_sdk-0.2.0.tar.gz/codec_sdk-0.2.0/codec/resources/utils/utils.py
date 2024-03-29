from codec.resources.utils.webhook import _verify_webhook
from typing import Union


class Utils:
    def __init__(self, auth):
        self.auth = auth

    def verify_webhook(
        self,
        secret: str,
        headers: Union[dict, str],
        payload: Union[dict, str]
    ):
        _verify_webhook(
            secret=secret,
            headers=headers,
            payload=payload
        )

