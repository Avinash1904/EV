from rest_framework import viewsets, status
from Profile.apis.serializers import ProfileSerializer, CreateProfileSerializer, HomeSerializer
from Profile.models import Profile
from ev.auth import FirebaseAuthentication
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from Profile.apis import permissions as custom_perm


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


# class HomeViewSet(viewsets.ModelViewSet):
#     queryset = Profile.objects.all()
#     serializer_class = HomeSerializer
