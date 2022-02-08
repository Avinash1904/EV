from rest_framework import serializers
from Profile.models import Profile
from Vehicle.models import Vehicle


class VehicleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Vehicle
        fields = ("uuid",)


class ProfileSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(source='user.email', read_only=True)
    organization_name = serializers.CharField(
        source='organization.name', read_only=True, allow_null=True)
    vehicles = VehicleSerializer(read_only=True, many=True)

    class Meta:
        model = Profile
        fields = (
            "uuid",
            "first_name",
            "last_name",
            "email",
            "phone_number",
            "ktp_number",
            "sim_number",
            "address",
            "profile_picture",
            "document_verification_status",
            "role",
            "organization_name",
            "vehicles",
        )
