from django.utils import timezone

from django.db import models
from django.contrib.auth.models import User
from django.db.models import Model


class Event(Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    subscribers = models.ManyToManyField(User, related_name='event_user')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    def is_future_event(self):
        return self.start_date > timezone.now()

    def is_past_event(self):
        print(self.end_date, timezone.now())
        return self.end_date < timezone.now()
