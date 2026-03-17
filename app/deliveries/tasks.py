from celery import shared_task
import requests
from django.utils import timezone
from apps.webhooks.models import Webhook
from apps.events.models import Event
from .models import Delivery
import hmac
import hashlib
import json

def generate_signature(secret, payload):
    return hmac.new(
        key=secret.encode(),
        msg=json.dumps(payload).encode(),
        digestmod=hashlib.sha256
    ).hexdigest()


@shared_task(bind=True, max_retries=3)
def send_webhook_task(self, webhook_id, event_id):
    webhook = Webhook.objects.get(id=webhook_id)
    event = Event.objects.get(id=event_id)

    delivery, _ = Delivery.objects.get_or_create(
        webhook=webhook,
        event=event
    )

    try:
        signature = generate_signature(webhook.secret, event.payload)

        response = requests.post(
            webhook.url,
            json=event.payload,
            headers={
                "X-Webhook-Signature": signature
            },
            timeout=5
        )

        delivery.status = "success"
        delivery.response_code = response.status_code
        delivery.response_body = response.text

    except Exception as exc:
        delivery.attempt_count += 1
        delivery.status = "failed"

        raise self.retry(exc=exc, countdown=2 ** delivery.attempt_count)

    finally:
        delivery.last_attempt_at = timezone.now()
        delivery.save()
