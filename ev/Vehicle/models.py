from django.db import models
from django.utils import timezone
from django.urls import reverse
from account.models import Organization, UUIDModel
from Profile.models import Profile
# Create your models here.


class Device(UUIDModel):
    imei_number = models.CharField(
        verbose_name="IMEI Number",
        max_length=100
    )
    device_type = models.CharField(
        verbose_name="device type",
        max_length=100
    )
    onboarding_date = models.DateTimeField(
        default=timezone.now,
        verbose_name="onboarding date"
    )

    def __str__(self):
        return self.imei_number

    def get_absolute_url(self):
        return reverse('device-list')


class Battery(UUIDModel):
    battery_number = models.CharField(
        verbose_name="battery number",
        max_length=50
    )
    capacity = models.CharField(
        verbose_name="battery capacity",
        max_length=100
    )
    onboarding_date = models.DateTimeField(
        default=timezone.now,
        verbose_name="onboarding date"
    )

    class Meta:
        verbose_name = "Battery"
        verbose_name_plural = "Batteries"

    def __str__(self):
        return self.battery_number

    def get_absolute_url(self):
        return reverse('battery-list')


class Vehicle(UUIDModel):
    vehicle_id = models.CharField(
        verbose_name="Vehicle Id",
        max_length=50
    )
    device = models.ForeignKey(
        Device,
        related_name="vehicle",
        verbose_name="device",
        on_delete=models.CASCADE
    )
    battery_id = models.ForeignKey(
        Battery,
        related_name="vehicle",
        on_delete=models.CASCADE,
        verbose_name="battery id",
        max_length=255
    )
    make = models.CharField(
        verbose_name="make",
        max_length=50
    )
    model = models.CharField(
        verbose_name="model",
        max_length=50
    )
    year = models.CharField(
        verbose_name="year",
        max_length=4
    )
    tag = models.CharField(
        verbose_name="tag",
        max_length=255,
        blank=True,
        null=True
    )
    created_at = models.DateTimeField(
        auto_now=True,
        verbose_name="created at"
        )
    organization = models.ForeignKey(
        Organization, related_name="vehicles", null=True, blank=True, on_delete=models.SET_NULL)

    profile = models.ForeignKey(
        Profile, related_name="vehicles", null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.vehicle_id

    def get_absolute_url(self):
        return reverse('vehicle-list')


class Driver(models.Model):
    name = models.CharField(
        verbose_name="driver name",
        max_length=255
    )
    phone_number = models.CharField(
        verbose_name="phone number",
        max_length=10
    )

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('driver-list')
