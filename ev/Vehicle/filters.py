import django_filters as filters
from .models import Vehicle, Battery, Device, Driver


class VehicleFilter(filters.FilterSet):
    search = filters.CharFilter(method="filter_search")

    class Meta:
        model = Vehicle
        fields = []

    def filter_search(self, queryset, name, value):
        return queryset.filter(vehicle_id__icontains=value)


class DeviceFilter(filters.FilterSet):
    search = filters.CharFilter(method="filter_search")

    class Meta:
        model = Device
        fields = []

    def filter_search(self, queryset, name, value):
        return queryset.filter(imei_number__icontains=value)


class BatteryFilter(filters.FilterSet):
    search = filters.CharFilter(method="filter_search")

    class Meta:
        model = Battery
        fields = []

    def filter_search(self, queryset, name, value):
        return queryset.filter(battery_number__icontains=value)


class DriverFilter(filters.FilterSet):
    search = filters.CharFilter(method="filter_search")

    class Meta:
        model = Driver
        fields = []

    def filter_search(self, queryset, name, value):
        return queryset.filter(name__icontains=value)
