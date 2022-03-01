from rest_framework import viewsets, status
from rest_framework.response import Response
from Vehicle.apis.serializers import (VehicleSerializer, BatterySerializer,
                                      DeviceSerializer, TripSerializer, LiveStatusSerializer)
from Vehicle.models import Vehicle, Battery, Device, Trip, LiveStatus
from django.utils import timezone
from ev.auth import FirebaseAuthentication
from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAuthenticated
from account.apis.viewsets import get_firebase_user_id
import logging
import datetime
import base64
import json
import requests
from rest_framework.decorators import action

# Create a logger for this file
logger = logging.getLogger(__file__)
errorLogger = logging.getLogger('error.'+__name__)


class VehicleViewset(viewsets.ModelViewSet):
    lookup_field = "uuid"
    queryset = Vehicle.objects.all()
    serializer_class = VehicleSerializer

    @action(detail=True, methods=("post",), url_path="start")
    def start(self, request, **kwargs):
        vehicle = self.get_object()
        device = vehicle.device
        command = "REMOTE_IGNITION_ON"
        device_imei = device.imei_number
        account_id = "109800"
        asset_uid = vehicle.device.vehicle_scl_id
        if device_imei and asset_uid:
            url = "https://api- aertrakasia.aeris.com/v1.0/api/things/assets/"+asset_uid+"/command"
            login_url = "https://api-aertrakasia.aeris.com/login"
            login_data = {
                "username": "aeris.krish+Rentalbanaran@gmail.com", "password": "Selis@123"}
            response = requests.post(login_url, data=login_data)
            if response.status_code == 200:
                print("status is 200")
                access_token = response.json()["access_token"]
                headers = {"token": access_token}
                req_data = {
                    "deviceId": device_imei,
                    "request": command,
                    "message": "testapi15",
                    "accountId": account_id,
                    "requestIdToOperateOn": "testapi15",
                    "activateAuxiliaryTracker": False
                }
                resp = requests.post(url=url, headers=headers, data=req_data)
                if resp.status_code == 200:
                    return Response({"status": True, "detail": "device started"}, status=status.HTTP_200_OK)
                return Response({"status": False, "detail": "device not started"}, status=status.HTTP_400_BAD_REQUEST)
            return Response({"status": False, "detail": "device not started"}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"status": False, "detail": "device not started"}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=("post",), url_path="stop")
    def stop(self, request, **kwargs):
        vehicle = self.get_object()
        device = vehicle.device
        command = "REMOTE_IGNITION_OFF"
        device_imei = device.imei_number
        account_id = "109800"
        asset_uid = vehicle.device.vehicle_scl_id
        if device_imei and asset_uid:
            url = "https://api- aertrakasia.aeris.com/v1.0/api/things/assets/"+asset_uid+"/command"
            login_url = "https://api-aertrakasia.aeris.com/login"
            login_data = {
                "username": "aeris.krish+Rentalbanaran@gmail.com", "password": "Selis@123"}
            response = requests.post(login_url, data=login_data)
            if response.status_code == 200:
                print("status is 200")
                access_token = response.json()["access_token"]
                headers = {"token": access_token}
                req_data = {
                    "deviceId": device_imei,
                    "request": command,
                    "message": "testapi15",
                    "accountId": account_id,
                    "requestIdToOperateOn": "testapi15",
                    "activateAuxiliaryTracker": False
                }
                resp = requests.post(url=url, headers=headers, data=req_data)
                if resp.status_code == 200:
                    return Response({"status": True, "detail": "device turned off"}, status=status.HTTP_200_OK)
                return Response({"status": False, "detail": "device not off"}, status=status.HTTP_400_BAD_REQUEST)
            return Response({"status": False, "detail": "device not off"}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"status": False, "detail": "device not off"}, status=status.HTTP_400_BAD_REQUEST)


class BatteryViewset(viewsets.ModelViewSet):
    lookup_field = "uuid"
    queryset = Battery.objects.all()
    serializer_class = BatterySerializer
    authentication_classes = [FirebaseAuthentication, ]
    permission_classes = [IsAuthenticated, ]

    def retrieve(self, request, *args, **kwargs):

        battery = self.get_object()
        serializer = self.serializer_class(
            battery, context=self.get_serializer_context())
        # grab live status data as well
        device_id = self.request.user.profile.vehicles.first().device.imei_number
        qs = LiveStatus.objects.filter(
            created_at=datetime.datetime.now().date(), device_id=device_id)
        live_status_serializer = LiveStatusSerializer(qs, many=True)
        data = live_status_serializer.data
        graph = []
        for d in data:
            voltage = d["battery_voltage"]
            voltage = int(voltage)/1000
            battery_min_voltage = battery.min_voltage
            battery_max_voltage = battery.max_voltage
            battery_percentage = (
                (battery_max_voltage-(voltage)) / (battery_max_voltage-battery_min_voltage))*100
            graph.append(battery_percentage)
        op = serializer.data.copy()
        op["graph"] = graph
        print("graph ", graph)
        return Response(op)


class DeviceViewset(viewsets.ModelViewSet):
    lookup_field = "uuid"
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer


class TripViewset(viewsets.ModelViewSet):
    lookup_field = "uuid"
    queryset = Trip.objects.all()
    serializer_class = TripSerializer
    authentication_classes = [FirebaseAuthentication, ]
    permission_classes = [IsAuthenticated, ]

    def get_queryset(self):
        profile = self.request.user.profile
        return Trip.objects.filter(created_by=profile)

    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        created_by = request.user.profile.uuid
        data["start"] = timezone.now()
        data["created_by"] = created_by
        serializer = self.get_serializer(data=data)
        if serializer.is_valid(True):
            serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.end is not None:
            return Response({"detail": "Trip is already ended"}, status=status.HTTP_409_CONFLICT)
        data = {}
        data["end"] = timezone.now()
        serializer = self.get_serializer(
            instance=instance, data=data, partial=True)
        serializer.is_valid(True)
        serializer.save()
        return Response(serializer.data)


class LiveStatusViewset(viewsets.ModelViewSet):
    queryset = LiveStatus.objects.all()
    serializer_class = LiveStatusSerializer

    def create(self, request, *args, **kwargs):
        #data = request.data.copy()
        encoded_data = request.data.get("message").get("data")
        message_bytes = base64.b64decode(encoded_data)
        decoded_data = json.loads(message_bytes.decode('utf-8'))
        data = {}
        location_time = decoded_data["data"].pop("locationTime", None)
        data['asset_uid'] = decoded_data["data"].pop("assetUid", None)
        data['latitude'] = decoded_data["data"].pop("latitude", None)
        data['longitude'] = decoded_data["data"].pop("longitude", None)
        data['device_id'] = decoded_data["data"].pop("deviceId", None)
        data['speed'] = decoded_data["data"].pop("speed", None)
        data['account_id'] = decoded_data["data"].pop("accountId", None)
        data['engine_state'] = decoded_data["data"].pop("engineState", None)
        data['battery_voltage'] = decoded_data["data"].pop(
            "assetBatteryVoltage", None)
        if location_time:
            epoch_time = location_time/1000
            date_time = datetime.datetime.fromtimestamp(epoch_time)
            # temp = location_time.split("T")
            captured_time = date_time.strftime("%Y-%m-%d-%H")
            # t1 = temp[0]
            # t2 = temp[1].split(":")[0]
            # captured_time = t1+"-"+t2
        data["data_capture_time"] = captured_time
        print("data ", data)
        # check if status for this time already exists
        try:
            ls = LiveStatus.objects.get(
                data_capture_time=captured_time, device_id=data['device_id'])
            serializer = self.get_serializer(
                instance=ls, data=data, partial=True)
            serializer.is_valid(True)
            serializer.save()
        except LiveStatus.DoesNotExist:
            # create new entry point
            serializer = self.get_serializer(data=data)
            if serializer.is_valid(True):
                serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)
