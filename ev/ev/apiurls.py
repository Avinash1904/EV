from rest_framework.routers import DefaultRouter
from django.urls import include, path
from Profile.apis.viewsets import ProfileViewset
router = DefaultRouter()
router.register("profiles", ProfileViewset, basename="profile")

urlpatterns = [
    path("", include(router.urls))
]
