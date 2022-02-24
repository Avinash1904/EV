from rest_framework import serializers
from Profile.models import Profile, Role
from Vehicle.apis.serializers import VehicleSerializer, TripSerializer
from rest_framework.reverse import reverse
from Vehicle.apis import helpers
from django.conf import settings


class ProfileSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source="uuid")
    email = serializers.EmailField(source='user.email', read_only=True)
    organization_name = serializers.CharField(
        source='organization.name', read_only=True, allow_null=True)
    # vehicles = VehicleSerializer(read_only=True, many=True)
    vehicles_url = serializers.SerializerMethodField()
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
            "vehicles_url",
            "trips_url",
        )

    def get_vehicles_url(self, profile):
        url = None
        request = self.context["request"]
        vehicle = profile.vehicles.first()
        if vehicle:
            vehicle_uuid = vehicle.uuid
            url = reverse("vehicles-detail",
                          kwargs={"uuid": vehicle_uuid}, request=request)

        return url

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


class HomeSerializer(serializers.ModelSerializer):
    home = serializers.SerializerMethodField()
    profile_url = serializers.SerializerMethodField()
    vehicles_url = serializers.SerializerMethodField()
    trips_url = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = (
            "home",
            "profile_url",
            "vehicles_url",
            "trips_url",
        )

    def get_trips_url(self, profile):
        request = self.context["request"]
        return reverse("trip-list", request=request)

    def get_profile_url(self, profile):
        request = self.context["request"]
        return reverse("profiles-detail", kwargs={"uuid": profile.uuid}, request=request)

    def get_vehicles_url(self, profile):
        url = None
        request = self.context["request"]
        vehicle = profile.vehicles.first()
        if vehicle:
            vehicle_uuid = vehicle.uuid
            url = reverse("vehicles-detail",
                          kwargs={"uuid": vehicle_uuid}, request=request)

        return url

    def get_home(self, profile):
        vehicle = profile.vehicles.first()
        data = {}
        if vehicle:
            data = helpers.get_info_by_vehicle(vehicle)
            data['facebook_url'] = settings.FACEBOOK_URL
            data['twitter_url'] = settings.TWITTER_URL
            data['instagram_url'] = settings.INSTAGRAM_URL
            data['profile_picture'] = profile.profile_picture.url
            data["full_name"] = profile.first_name + " " + profile.last_name
        else:
            data['facebook_url'] = settings.FACEBOOK_URL
            data['twitter_url'] = settings.TWITTER_URL
            data['instagram_url'] = settings.INSTAGRAM_URL
            data['profile_picture'] = profile.profile_picture.url
            data["full_name"] = profile.first_name + " " + profile.last_name
        return data
