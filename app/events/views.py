from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Event
from apps.webhooks.models import Webhook
from apps.deliveries.tasks import send_webhook_task

class EventCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        event = Event.objects.create(
            event_type=request.data["event_type"],
            payload=request.data["payload"]
        )

        webhooks = Webhook.objects.filter(
            event_type=event.event_type,
            is_active=True
        )

        for webhook in webhooks:
            send_webhook_task.delay(webhook.id, event.id)

        return Response({"message": "Event created and queued"})
