from drf_yasg.utils import swagger_auto_schema, no_body
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.decorators import permission_classes as perm_classes
from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework.response import Response

from event.filters import ProductFilter
from event.models import Event
from event.permissions import OwnEventPermission
from event.serializers import EventSerializer


class EventViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated, OwnEventPermission)
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    filterset_class = ProductFilter

    @swagger_auto_schema(request_body=no_body, responses={
        404: "Not found",
        400: "Bad request",
        200: "You have been registered"
    })
    @action(detail=True, methods=['post'])
    @perm_classes((IsAuthenticated,))
    def register(self, request, *args, **kwargs):
        event = self.get_object()
        user = request.user

        if event.is_past_event():
            raise ValidationError("You can't register for past event")

        if user in event.subscribers.all():
            return Response(
                {
                    "detail": "You are already registered"
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        event.subscribers.add(user)
        return Response(
            {
                "detail": "You have been registered for the event"
            },
            status=status.HTTP_200_OK
        )

    @swagger_auto_schema(request_body=no_body, responses={
        404: "Not found",
        400: "Bad request",
        200: "You have been unregistered"
    })
    @action(detail=True, methods=['post'])
    @perm_classes((IsAuthenticated, ))
    def unregister(self, request, *args, **kwargs):
        event = self.get_object()
        user = request.user

        if event.is_past_event():
            raise ValidationError("You cannot unregister from past event")

        if user not in event.subscribers.all():
            return Response(
                {
                    "detail": "You are not registered for this event"
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        event.subscribers.remove(user)
        return Response(
            {
                "detail": "You have been unregistered from the event"
            },
            status=status.HTTP_200_OK
        )

