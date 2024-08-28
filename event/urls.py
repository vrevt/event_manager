from rest_framework import routers

from event.views import EventViewSet

router = routers.DefaultRouter()
router.register(r'events', EventViewSet, basename="events")
