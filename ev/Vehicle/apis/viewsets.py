from rest_framework import viewsets, status
from rest_framework.response import Response
from Vehicle.apis.serializers import VehicleSerializer, BatterySerializer, DeviceSerializer, TripSerializer
from Vehicle.models import Vehicle, Battery, Device, Trip
from django.utils import timezone
from ev.auth import FirebaseAuthentication
from rest_framework.permissions import IsAuthenticated


class VehicleViewset(viewsets.ModelViewSet):
    lookup_field = "uuid"
    queryset = Vehicle.objects.all()
    serializer_class = VehicleSerializer


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
