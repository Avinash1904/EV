from rest_framework import viewsets, status
from rest_framework.response import Response
from Vehicle.apis.serializers import (VehicleSerializer, BatterySerializer,
                                      DeviceSerializer, TripSerializer, LiveStatusSerializer)
from Vehicle.models import Vehicle, Battery, Device, Trip, LiveStatus
from django.utils import timezone
from ev.auth import FirebaseAuthentication
from rest_framework.permissions import IsAuthenticated


class VehicleViewset(viewsets.ModelViewSet):
    lookup_field = "uuid"
    queryset = Vehicle.objects.all()
    serializer_class = VehicleSerializer

    # @action(detail=True, methods=("post",), url_path="start")
    # def start(self, request, **kwargs):
    #     vehicle = self.get_object()
    #     device = vehicle.device
    #     command = "REMOTE_IGNITION_OFF"
    # {
    # "deviceId": "Device_IMEI",
    # "request": "REMOTE_IGNITION_OFF",   // Command need to be executed OFF/ON
    # "message": "testapi15",
    # "accountId": Account_ID,   // Account ID in which device is provisioned
    # "requestIdToOperateOn": "testapi15",
    # "activateAuxiliaryTracker": false
    # }


class BatteryViewset(viewsets.ModelViewSet):
    lookup_field = "uuid"
    queryset = Battery.objects.all()
    serializer_class = BatterySerializer


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
        data = request.data.copy()
        location_time = data.pop("locationTime", None)
        data['asset_uid'] = data.pop("locationTime", None)
        data['latitude'] = data.pop("latitude", None)
        data['longitude'] = data.pop("longitude", None)
        data['device_id'] = data.pop("deviceId", None)
        data['speed'] = data.pop("speed", None)
        data['account_id'] = data.pop("accountId", None)
        data['engine_state'] = data.pop("engineState", None)
        data['battery_voltage'] = data.pop("assetBatteryVoltage", None)
        if location_time:
            temp = location_time.split("T")
            t1 = temp[0]
            t2 = temp[1].split(":")[0]
            captured_time = t1+"-"+t2
        data["captured_time"] = captured_time
        # check if status for this time already exists
        try:
            ls = LiveStatus.objects.get(
                captured_time=captured_time, device_id=data['device_id'])
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
