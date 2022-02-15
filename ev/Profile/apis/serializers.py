from rest_framework import serializers
from Profile.models import Profile
from Vehicle.apis.serializers import VehicleSerializer


class ProfileSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source="uuid")
    email = serializers.EmailField(source='user.email', read_only=True)
    organization_name = serializers.CharField(
        source='organization.name', read_only=True, allow_null=True)
    vehicles = VehicleSerializer(read_only=True, many=True)
    url = serializers.HyperlinkedIdentityField(
        view_name="profiles-detail", lookup_field="uuid")
    role = serializers.CharField(
        source='role.name', read_only=True, allow_null=True)

    class Meta:
        model = Profile
        fields = (
            "id",
            "url",
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


class CreateProfileSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source="uuid")

    class Meta:
        model = Profile
        fields = (
            "id",
            "first_name",
            "last_name",
            "address",
        )

    def create(self, validated_data):
        print("going for profile creation ..")
        user = self.context["request"].user
        profile = Profile(**validated_data)
        profile.user = user
        profile.save()
        return profile
