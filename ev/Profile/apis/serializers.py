from rest_framework import serializers
from Profile.models import Profile, Role
from Vehicle.apis.serializers import VehicleSerializer, TripSerializer
from rest_framework.reverse import reverse


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
    phone_number = serializers.SerializerMethodField()
    trips_url = serializers.SerializerMethodField()

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
            "ktp_image",
            "sim_image",
            "document_verification_status",
            "role",
            "organization_name",
            "vehicles",
            "trips_url",
        )

    def get_phone_number(self, profile):
        return profile.user.phone_number

    def get_trips_url(self, profile):
        request = self.context["request"]
        return reverse("trip-list", request=request)


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
        profile.role = Role.objects.get(id=1)
        profile.save()
        return profile
