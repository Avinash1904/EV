from django.contrib import admin

# Register your models here.
from django_google_maps import widgets as map_widgets
from django_google_maps import fields as map_fields
from .models import *


@admin.register(GoogleMap)
class GoogleMapAdmin(admin.ModelAdmin):
    formfield_overrides = {
        map_fields.AddressField: {'widget': map_widgets.GoogleMapsAddressWidget},
    }