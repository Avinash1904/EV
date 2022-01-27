import django_filters as filters
from .models import Profile


class ProfileFilter(filters.FilterSet):
    search = filters.CharFilter(method="filter_search")

    class Meta:
        model = Profile
        fields = []

    def filter_search(self, queryset, name, value):
        return queryset.filter(name__icontains=value)
