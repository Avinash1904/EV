import requests


def get_info_by_vehicle(vehicle):
    data = {}
    if not vehicle:
        data['battery_percentage'] = None
        data["used_percentage"] = None
        data["estimated_distance"] = None
        data["latitude"] = None
        data["longitude"] = None
        return data

    login_url = "https://api-aertrakasia.aeris.com/login"
    login_data = {
        "username": "aeris.krish+Rentalbanaran@gmail.com", "password": "Selis@123"}
    response = requests.post(login_url, data=login_data)
    if response.status_code == 200:
        print("status is 200")
        access_token = response.json()["access_token"]

        device_url = "https://api-aertrakasia.aeris.com/v1.0/api/things/accounts/latestStatus?deviceId=" + \
            vehicle.device.imei_number
        headers = {"token": access_token}
        deviceInfo = requests.get(device_url, headers=headers)
        count = 0
        device = deviceInfo.json()[0]
        battery = device["batteryVoltage"][1]
        val = battery["value"] if battery["value"] is not None else 0
        voltage = val/100
        if voltage:
            battery_min_voltage = vehicle.battery_id.min_voltage
            battery_max_voltage = vehicle.battery_id.max_voltage
            old_range = battery_max_voltage - battery_min_voltage
            new_range = 10
            # battery_percentage = (
            #     ((voltage-battery_min_voltage)*new_range)/old_range)
            print("voltage is ", (voltage))
            print("max is ", battery_max_voltage)
            print("min is ", battery_min_voltage)
            battery_percentage = ((battery_max_voltage-(voltage))
                                  / (battery_max_voltage-battery_min_voltage))*100
            used_percentage = 100-battery_percentage

            # calculate estimated distance
            distance = (battery_percentage
                        * vehicle.battery_id.max_distance)/100
            data['battery_percentage'] = battery_percentage
            data["used_percentage"] = used_percentage
            data["estimated_distance"] = distance
        else:
            data['battery_percentage'] = None
            data["used_percentage"] = None
            data["estimated_distance"] = None

        data["latitude"] = device["validLatitude"]
        data["longitude"] = device["validLongitude"]

        return data

        # for device in deviceInfo.json():
        #     print("device Id ", device["deviceId"])
        #     count += 1
        #     if str(device["deviceId"]) == vehicle.device.imei_number:
        #         # get battery voltage
        #         print("device is ", device)
        #         battery = device["batteryVoltage"][1]
        #         val = battery["value"] if battery["value"] is not None else 0
        #         voltage = val/100
        #         if voltage:
        #             battery_min_voltage = vehicle.battery_id.min_voltage
        #             battery_max_voltage = vehicle.battery_id.max_voltage
        #             old_range = battery_max_voltage - battery_min_voltage
        #             new_range = 10
        #             # battery_percentage = (
        #             #     ((voltage-battery_min_voltage)*new_range)/old_range)
        #             print("voltage is ", (voltage))
        #             print("max is ", battery_max_voltage)
        #             print("min is ", battery_min_voltage)
        #             battery_percentage = ((battery_max_voltage-(voltage))
        #                                   / (battery_max_voltage-battery_min_voltage))*100
        #             used_percentage = 100-battery_percentage
        #
        #             # calculate estimated distance
        #             distance = (battery_percentage
        #                         * vehicle.battery_id.max_distance)/100
        #             data['battery_percentage'] = battery_percentage
        #             data["used_percentage"] = used_percentage
        #             data["estimated_distance"] = distance
        #         else:
        #             data['battery_percentage'] = None
        #             data["used_percentage"] = None
        #             data["estimated_distance"] = None
        #
        #         data["latitude"] = device["validLatitude"]
        #         data["longitude"] = device["validLongitude"]
        #
        #         return data
    return None


def get_battery_voltage(vehicle):
    login_url = "https://api-aertrakasia.aeris.com/login"
    login_data = {
        "username": "aeris.krish+Rentalbanaran@gmail.com", "password": "Selis@123"}
    response = requests.post(login_url, data=login_data)
    if response.status_code == 200:
        print("status is 200")
        access_token = response.json()["access_token"]

        device_url = "https://api-aertrakasia.aeris.com/v1.0/api/things/accounts/latestStatus?deviceId=" + \
            vehicle.device.imei_number
        headers = {"token": access_token}
        deviceInfo = requests.get(device_url, headers=headers)
        if deviceInfo.status_code == 200:
            device = deviceInfo.json()[0]
            print("device ", device)
            battery = device["batteryVoltage"][1]
            val = battery["value"] if battery["value"] is not None else 0
            voltage = val/100
            return voltage

        # count = 0
        # for device in deviceInfo.json():
        #     print("device Id ", device["deviceId"])
        #     count += 1
        #     if str(device["deviceId"]) == vehicle.device.imei_number:
        #         # get battery voltage
        #         print("device is ", device)
        #         battery = device["batteryVoltage"][1]
        #         val = battery["value"] if battery["value"] is not None else 0
        #         voltage = val/100
        #         return voltage
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
        # battery_percentage = (
        #     ((voltage-battery_min_voltage)*new_range)/old_range)
        print("voltage is ", (voltage/100))
        battery_percentage = ((battery_max_voltage-(voltage/10))
                              / (battery_max_voltage-battery_min_voltage))*100
        used_percentage = 100-battery_percentage

        # calculate estimated distance
        distance = (battery_percentage*vehicle.battery_id.max_distance)/100
        data['battery_percentage'] = battery_percentage
        data["used_percentage"] = used_percentage
        data["estimated_distance"] = distance
        return data
    data['battery_percentage'] = None
    data["used_percentage"] = None
    data["estimated_distance"] = None

    return data


def get_device_info(dev):
    op = {}
    op["latitude"] = None
    op["longitude"] = None
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
            if str(device["deviceId"]) == dev.imei_number:
                # get battery voltage
                print("device is ", device)
                op["latitude"] = device["validLatitude"]
                op["longitude"] = device["validLongitude"]

    return op
