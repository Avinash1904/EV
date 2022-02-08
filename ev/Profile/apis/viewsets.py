from rest_framework import viewsets
from Profile.apis.serializers import ProfileSerializer
from Profile.models import Profile


class ProfileViewset(viewsets.ModelViewSet):
    lookup_field = "uuid"
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
