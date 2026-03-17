import hmac
import hashlib
import json

def generate_signature(secret: str, payload: dict) -> str:
    """
    Generate HMAC SHA256 signature for webhook payload
    """
    return hmac.new(
        key=secret.encode(),
        msg=json.dumps(payload, separators=(",", ":")).encode(),
        digestmod=hashlib.sha256,
    ).hexdigest()
