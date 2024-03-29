from svix.webhooks import Webhook, WebhookVerificationError
from codec.exceptions import WebhookException
import json


def _verify_webhook(secret, headers, payload):
    if isinstance(headers, str):
        headers = json.loads(headers)
    elif isinstance(headers, dict):
        pass
    
    if isinstance(payload, dict):
        payload = json.dumps(payload, separators=(",", ":"))
    elif isinstance(payload, str):
        pass
    
    wh = Webhook(secret)
    
    try:
        wh.verify(payload, headers)
    except WebhookVerificationError as e:
        raise WebhookException(str(e))

