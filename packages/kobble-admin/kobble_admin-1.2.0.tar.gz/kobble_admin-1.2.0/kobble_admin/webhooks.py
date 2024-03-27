import hmac
import json
from dataclasses import dataclass


@dataclass
class WebhookEvent:
    type: str
    data: dict


class KobbleWebhooks:
    def __init__(self):
        pass

    def construct_event(self, body: bytes | bytearray | str, signature: str, secret: str):
        transformed_body = None

        if isinstance(body, str):
            transformed_body = bytes(body, "utf-8")
        else:
            transformed_body = bytes(body)

        constructed_sig = hmac.new(
            key=bytes.fromhex(secret),
            msg=transformed_body,
            digestmod="sha256"
        ).digest().hex()

        if constructed_sig != signature:
            raise Exception(
                "Failed to verify signature: did you pass the correct secret?"
            )

        payload = json.loads(body)

        return WebhookEvent(type=payload["type"], data=payload["data"])
