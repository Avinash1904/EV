from django.forms import ModelForm
from .models import Vehicle, Battery, Device, Driver


class VehicleForm(ModelForm):
    class Meta:
        model = Vehicle
        fields = ("vehicle_id", "make", "model",
                  "battery_id", "device", "year", "tag")


class VehicleUpdateForm(ModelForm):
    class Meta:
        model = Vehicle
        fields = ("vehicle_id", "make", "model",
                  "battery_id", "device", "year", "tag")


class BatteryForm(ModelForm):
    class Meta:
        model = Battery
        fields = '__all__'


class DeviceForm(ModelForm):
    class Meta:
        model = Device
        fields = '__all__'


class DriverForm(ModelForm):
    class Meta:
        model = Driver
        fields = '__all__'
