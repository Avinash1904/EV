import requests


def get_battery_voltage(vehicle):
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
        for device in deviceInfo.json():
            print("device Id ", device["deviceId"])
            count += 1
            if str(device["deviceId"]) == vehicle.device.imei_number:
                # get battery voltage
                print("device is ", device)
                battery = device["batteryVoltage"][1]
                val = battery["value"] if battery["value"] is not None else 0
                voltage = val/100
                return voltage
    return None


def get_battery_info(vehicle):
    voltage = get_battery_voltage(vehicle)
    data = {}
    if voltage:
        # get current battery level
        battery_min_voltage = vehicle.battery_id.min_voltage
        battery_max_voltage = vehicle.battery_id.max_voltage
        old_range = battery_max_voltage - battery_min_voltage
        new_range = 10
        battery_percentage = (
            ((voltage-battery_min_voltage)*new_range)/old_range)
        used_percentage = 100-battery_percentage

        # calculate estimated distance
        distance = (battery_percentage*vehicle.battery_id.max_distance)/100
        data['battery_percentage'] = battery_percentage
        data["used_percentage"] = used_percentage
        data["distance"] = distance
        return data
    data['battery_percentage'] = None
    data["used_percentage"] = None
    data["distance"] = None

    return data
