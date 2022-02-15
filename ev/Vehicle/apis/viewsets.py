from rest_framework import viewsets
from Vehicle.apis.serializers import VehicleSerializer
from Vehicle.models import Vehicle


class VehicleViewset(viewsets.ModelViewSet):
    lookup_field = "uuid"
    queryset = Vehicle.objects.all()
    serializer_class = VehicleSerializer
