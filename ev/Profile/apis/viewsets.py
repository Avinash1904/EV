from rest_framework import viewsets
from Profile.apis.serializers import ProfileSerializer, CreateProfileSerializer
from Profile.models import Profile
from ev.auth import FirebaseAuthentication
from rest_framework.permissions import IsAuthenticated


class ProfileViewset(viewsets.ModelViewSet):
    lookup_field = "uuid"
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    authentication_classes = [FirebaseAuthentication, ]
    permission_classes = [IsAuthenticated, ]

    def get_serializer_class(self):
        if self.request.method == "POST":
            return CreateProfileSerializer
        return ProfileSerializer
