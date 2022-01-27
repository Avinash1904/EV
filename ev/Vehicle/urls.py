
from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import TemplateView
from django.conf import settings
from django.conf.urls.static import static
from .views import *

admin.site.site_header = " "
# admin.site.site_title = "Admin Console"
admin.site.index_title = "Admin Console"
urlpatterns = [
    path('vehicle/', VehicleListView.as_view(), name='vehicle-list'),
    path('create/', vehicleCreateView.as_view(), name='vehicle-create'),
    path('<pk>/update/', VehicleUpdateView.as_view(), name='vehicle-update'),
    path('<pk>/delete/', VehicleDeleteView.as_view(), name='vehicle-delete'),

    path('battery/', BatteryListView.as_view(), name='battery-list'),
    path('battery/create/', BatteryCreateView.as_view(), name='battery-create'),
    path('battery/<pk>/update/', BatteryUpdateView.as_view(), name='battery-update'),
    path('battery/<pk>/delete/', BatteryDeleteView.as_view(), name='battery-delete'),

    path('device/', DeviceListView.as_view(), name='device-list'),
    path('device/create/', DeviceCreateView.as_view(), name='device-create'),
    path('device/<pk>/update/', DeviceUpdateView.as_view(), name='device-update'),
    path('device/<pk>/delete/', DeviceDeleteView.as_view(), name='device-delete'),

    path('driver/', DriverListView.as_view(), name='driver-list'),
    path('driver/create/', driver_registration_view, name='driver-create'),
    path('driver/<pk>/update/', DriverUpdateView.as_view(), name='driver-update'),
    path('driver/<pk>/delete/', DriverDeleteView.as_view(), name='driver-delete'),

    path('battery-autocomplete/', BatteryAutocomplete.as_view(),
         name="battery-autocomplete"),
    path('device-autocomplete/', DeviceAutocomplete.as_view(),
         name="device-autocomplete"),
]
