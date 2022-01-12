from django.forms import ModelForm
from .models import Vehicle


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
