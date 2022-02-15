from rest_framework import serializers
from Vehicle.models import Vehicle, Battery, Device
from Vehicle.apis import helpers


class BatterySerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source="uuid")

    class Meta:
        model = Battery
        fields = (
            "id",
            "battery_number",
            "capacity",
        )


class DeviceSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source="uuid")

    class Meta:
        model = Device
        fields = (
            "id",
            "imei_number",
            "device_type",
        )


class VehicleSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source="uuid")
    url = serializers.HyperlinkedIdentityField(
        view_name="vehicles-detail", lookup_field="uuid")
    battery = BatterySerializer(
        read_only=True, allow_null=True, source="battery_id")
    battery_info = serializers.SerializerMethodField()
    device = DeviceSerializer(read_only=True, allow_null=True)
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
            "battery_info",
        )

    def get_battery_info(self, vehicle):
        data = helpers.get_battery_info(vehicle)
        return data
