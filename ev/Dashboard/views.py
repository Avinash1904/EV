from django.shortcuts import render
import requests
from geopy.geocoders import Nominatim
from datetime import datetime
import pytz

# Create your views here.


def map(request):
    # make api call to get token
    geolocator = Nominatim(user_agent="imoto")
    locations = []
    login_url = "https://api-aertrakasia.aeris.com/login"
    login_data = {"username": "poc.gelis1@gmail.com", "password": "Aeris@123"}
    response = requests.post(login_url, data=login_data)
    if response.status_code == 200:
        access_token = response.json()["access_token"]

        device_url = "https://api-aertrakasia.aeris.com/v1.0/api/things/accounts/latestStatus"
        headers = {"token": access_token}
        deviceInfo = requests.get(device_url, headers=headers)

        for device in deviceInfo.json():
            data = []
            if device["validLatitude"]:
                location = geolocator.reverse(
                    str(device["validLatitude"])+", "+str(device["validLongitude"]))
                address = location.address
                time = device["updateTime"]
                indonesia_time = datetime.fromtimestamp(time)
                vehicle_name = device['vehicleName']
                data.append(vehicle_name)
                data.append(address)
                data.append(str(indonesia_time))
                data.append(device["validLatitude"])
                data.append(device["validLongitude"])

                locations.append(data)

        print("locations ", locations)

    context = {
        "locations": locations
    }
    # return render(request, "admin/live_maps.html", context=context)
    return render(request, "dashboard/live_map.html", context=context)
