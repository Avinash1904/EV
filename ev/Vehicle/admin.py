from django.contrib import admin
from .models import *
# Register your models here.
@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    list_display = (
        "vehicle_id",
        "make",
        "model",
        "battery_id",
    )

@admin.register(Battery)
class BatteryAdmin(admin.ModelAdmin):
    list_display = (
        "battery_number",
        "capacity",
    )


@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
    list_display = (
        "imei_number",
        "device_type",
    )
# admin.site.register(Battery)
admin.site.register(Driver)
