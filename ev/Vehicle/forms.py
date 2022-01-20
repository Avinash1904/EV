from django.forms import ModelForm
from .models import Vehicle, Battery, Device, Driver
from django.contrib.auth.forms import UserCreationForm
from django import forms
from account.models import Account


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


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(
        max_length=100, help_text="Required. Add a valid email address.")

    class Meta:
        model = Account
        fields = ("email", "password1", "password2")
