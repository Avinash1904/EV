from django.db import models

# Create your models here.
from django_google_maps import fields as map_fields

class GoogleMap(models.Model):
    address = map_fields.AddressField(max_length=200)
    geolocation = map_fields.GeoLocationField(max_length=100)

    class Meta:
        verbose_name = "Live"
        verbose_name_plural = "Live"