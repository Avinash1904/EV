import django_filters as filters
from .models import Organization


class OrganizationFilter(filters.FilterSet):
    search = filters.CharFilter(method="filter_search")

    class Meta:
        model = Organization
        fields = []

    def filter_search(self, queryset, name, value):
        return queryset.filter(vehicle_id__icontains=value)
