from django_filters import rest_framework as filters

from event.models import Event


class ProductFilter(filters.FilterSet):
    class Meta:
        model = Event
        fields = ['name', 'description', 'created_by']

