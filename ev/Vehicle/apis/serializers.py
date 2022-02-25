from rest_framework import serializers
from Vehicle.models import Vehicle, Battery, Device, Trip
from Vehicle.apis import helpers
from Profile.models import Profile


class TripSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source="uuid")
    url = serializers.HyperlinkedIdentityField(
        view_name="trip-detail", lookup_field="uuid")
    created_by = serializers.SlugRelatedField(
        queryset=Profile.objects.all(),
        slug_field="uuid",
        required=True
    )

    class Meta:
        model = Trip
        fields = (
            "id",
            "url",
            "source",
            "destination",
            "start",
            "end",
            "created_by",
        )


class BatterySerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source="uuid")
    url = serializers.HyperlinkedIdentityField(
        view_name="battery-detail", lookup_field="uuid")
    battery_percentage = serializers.SerializerMethodField()
    used_percentage = serializers.SerializerMethodField()
    estimated_range = serializers.SerializerMethodField()
    battery_cycle = serializers.SerializerMethodField()
    battery_temprature = serializers.SerializerMethodField()
    battery_score = serializers.SerializerMethodField()
    # data = None

    class Meta:
        model = Battery
        fields = (
            "id",
            "url",
            "battery_number",
            "capacity",
            "battery_percentage",
            "used_percentage",
            "estimated_range",
            "battery_cycle",
            "battery_temprature",
            "battery_score",

        )

    def get_battery_percentage(self, battery):
        print("/n/n vehicle ", battery.vehicle.first())
        data = helpers.get_battery_info(battery.vehicle.first())
        # self.data = data
        return data["battery_percentage"]

    def get_used_percentage(self, battery):
        data = helpers.get_battery_info(battery.vehicle.first())
        return data["used_percentage"]

    def get_estimated_range(self, battery):
        data = helpers.get_battery_info(battery.vehicle.first())
        return data["estimated_distance"]

    def get_battery_score(self, battery):
        return None

    def get_battery_temprature(self, battery):
        return None

    def get_battery_cycle(self, battery):
        return None


class DeviceSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source="uuid")
    latitude = serializers.SerializerMethodField()
    longitude = serializers.SerializerMethodField()

    class Meta:
        model = Device
        fields = (
            "id",
            "imei_number",
            "device_type",
            "latitude",
            "longitude",
        )

    def get_latitude(self, device):
        data = helpers.get_device_info(device)
        return data["latitude"]

    def get_longitude(self, device):
        data = helpers.get_device_info(device)
        return data["longitude"]


class VehicleSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source="uuid")
    url = serializers.HyperlinkedIdentityField(
        view_name="vehicles-detail", lookup_field="uuid")
    battery = BatterySerializer(
        read_only=True, allow_null=True, source="battery_id")
    device = DeviceSerializer(read_only=True, allow_null=True)
    total_distance_travelled = serializers.SerializerMethodField()
    total_time_travelled = serializers.SerializerMethodField()
    # device = serializers.ReadOnlyField(source="device.imei_number")

    class Meta:
        model = Vehicle
        fields = (
            "id",
            "url",
            "vehicle_id",
            "make",
            "model",
            "year",
            "battery",
            "device",
            "total_distance_travelled",
            "total_time_travelled",
            "vin_number",
        )

    def get_total_time_travelled(self, vehicle):
        return None

    def get_total_distance_travelled(self, vehicle):
        return None
