from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/users/", include("app.users.urls")),
    path("api/events/", include("app.events.urls")),
    path("api/deliveries/", include("app.deliveries.urls")),
    path("api/webhooks/", include("app.webhooks.urls")),
]
