from django.shortcuts import render
import requests

# Create your views here.

def map(request):
    # make api call to get token
    locations = []
    login_url = "https://api-aertrakasia.aeris.com/login"
    login_data = {"username":"poc.gelis1@gmail.com", "password":"Aeris@123"}
    response = requests.post(login_url, data=login_data)
    if response.status_code == 200:
        access_token = response.json()["access_token"]

        device_url = "https://api-aertrakasia.aeris.com/v1.0/api/things/accounts/latestStatus"
        headers = {"token":access_token}
        deviceInfo = requests.get(device_url, headers=headers)


        for device in deviceInfo.json():
            data = []
            data.append(device["deviceId"])
            data.append(device["validLatitude"])
            data.append(device["validLongitude"])
            if device["validLatitude"]:
                locations.append(data)

        print("locations ", locations)

    context = {
        "locations": locations
    }
    return render(request, "admin/live_maps.html", context=context)
