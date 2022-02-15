from rest_framework import serializers
from account.models import Account
from Profile.models import Profile
from django.conf import settings


class CreateProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = (
            "first_name",
            "last_name",
            "phone_number"
        )


class CreateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = (
            "email",
            "phone_number",
            "firebase_uid"
        )

    def create(self, validated_data):
        user = Account(**validated_data)
        user.set_password(settings.SECRET_KEY)
        user.save()

        return user
