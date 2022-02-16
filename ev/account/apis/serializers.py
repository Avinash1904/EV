from rest_framework import serializers
from account.models import Account
from Profile.models import Profile
from django.conf import settings
from rest_framework.reverse import reverse
from django.db import transaction


class CreateUserSerializer(serializers.ModelSerializer):
    profile_url = serializers.SerializerMethodField()
    first_name = serializers.CharField(write_only=True)
    last_name = serializers.CharField(write_only=True)

    class Meta:
        model = Account
        fields = (
            "email",
            "phone_number",
            "firebase_uid",
            "profile_url",
            "first_name",
            "last_name",
        )

    def get_profile_url(self, user):
        request = self.context["request"]
        return reverse("profiles-detail", kwargs={"uuid": user.profile.uuid}, request=request)

    @transaction.atomic
    def create(self, validated_data):
        first_name = validated_data.pop("first_name")
        last_name = validated_data.pop("last_name")
        user = Account(**validated_data)
        user.set_password(settings.SECRET_KEY)
        user.save()
        # data = self.context["request"].data

        profile = Profile(first_name=first_name,
                          last_name=last_name, user=user)
        profile.save()

        return user
