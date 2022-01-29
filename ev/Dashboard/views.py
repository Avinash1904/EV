from django.shortcuts import render
import requests
from geopy.geocoders import Nominatim
from datetime import datetime
import pytz
from django.conf import settings
from ev.permissions import admin_or_manager_only
from Vehicle.models import Vehicle
# Create your views here.


@admin_or_manager_only
def map(request):
    # make api call to get token
    vehicles_devices_list = None
    if request.user.is_admin:
        vehicles_devices_list = list(Vehicle.objects.all().values_list(
            "device_id__imei_number", flat=True))
    else:
        vehicles_devices_list = list(Vehicle.objects.all().values_list(
            "device_id__imei_number", flat=True))
    locations = []
    login_url = "https://api-aertrakasia.aeris.com/login"
    login_data = {
        "username": "aeris.krish+Rentalbanaran@gmail.com", "password": "Selis@123"}
    response = requests.post(login_url, data=login_data)
    if response.status_code == 200:
        print("status is 200")
        access_token = response.json()["access_token"]

        device_url = "https://api-aertrakasia.aeris.com/v1.0/api/things/accounts/latestStatus"
        headers = {"token": access_token}
        deviceInfo = requests.get(device_url, headers=headers)
        count = 0
        print("vehicles_devices_list ", vehicles_devices_list)

        for device in deviceInfo.json():
            print("device Id ", device["deviceId"])
            count += 1
            data = []
            if device["validLatitude"]:
                print(" valid lat")
                if str(device["deviceId"]) in vehicles_devices_list:
                    vehicle_name = Vehicle.objects.get(
                        device__imei_number=str(device["deviceId"])).vehicle_id
                    print("found ..")
                    address = "Unknown"
                    time = device["updateTime"]
                    indonesia_time = datetime.fromtimestamp(time)
                    #vehicle_name = device['vehicleName']
                    data.append(vehicle_name)
                    data.append(address)
                    data.append(str(indonesia_time))
                    data.append(device["validLatitude"])
                    data.append(device["validLongitude"])
                    locations.append(data)
        print("count ", count)

        # print("locations ", locations)

    context = {
        "locations": locations
    }
    # return render(request, "admin/live_maps.html", context=context)
    return render(request, "dashboard/live_map.html", context=context)
