from rest_framework import viewsets, status
from Profile.apis.serializers import ProfileSerializer, CreateProfileSerializer, HomeSerializer
from account.models import Account
from Profile.models import Profile
from ev.auth import FirebaseAuthentication
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from Profile.apis import permissions as custom_perm
from rest_framework import views
from django.db import IntegrityError


class ProfileViewset(viewsets.ModelViewSet):
    lookup_field = "uuid"
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    authentication_classes = [FirebaseAuthentication, ]
    permission_classes = [IsAuthenticated, custom_perm.ProfilePermission]

    def get_serializer_class(self):
        if self.request.method == "POST":
            return CreateProfileSerializer
        return ProfileSerializer

    def retrieve(self, request, uuid=None):
        print("user is ", request.user)
        op = {}
        op["status"] = True
        op["data"] = {}
        op["detail"] = {}
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        op["data"] = serializer.data
        return Response(op, status=status.HTTP_200_OK)

    def partial_update(self, request, *args, **kwargs):
        profile = self.get_object()
        data = {}
        data = request.data.copy()
        phone_number = data.pop('phone_number', None)
        country_code = data.pop("country_code", None)
        email = data.pop("email", None)
        if email or phone_number or country_code:
            user = profile.user
            if phone_number:
                user.phone_number = phone_number
            if email:
                user.email = email
            if country_code:
                user.country_code = country_code
            try:
                user.save()
            except IntegrityError as e:
                return Response({"detail": e.args[0].split(":")[-1].split(".")[-1] + " already exists"}, status=status.HTTP_409_CONFLICT)

        serializer = self.get_serializer(
            instance=profile, data=data, partial=True)
        serializer.is_valid(True)
        serializer.save()
        return Response(serializer.data)


class HomeViewSet(viewsets.ModelViewSet):
    lookup_field = "uuid"
    queryset = Profile.objects.all()
    serializer_class = HomeSerializer
    authentication_classes = [FirebaseAuthentication, ]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Profile.objects.filter(user=self.request.user)

    def list(self, request, *args, **kwargs):
        serializer = self.get_serializer(
            self.request.user.profile, context=self.get_serializer_context()
        )
        # serializer = serializer_class(
        #     self.request.user.profile, request=request)
        # data = serializer.data['home']
        return Response(serializer.data)
