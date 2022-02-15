from rest_framework.routers import DefaultRouter
from django.urls import include, path
from Profile.apis.viewsets import ProfileViewset
from Vehicle.apis.viewsets import VehicleViewset
from account.apis.viewsets import UserViewset

router = DefaultRouter()
router.register("profiles", ProfileViewset, basename="profiles")
router.register("vehicles", VehicleViewset, basename="vehicles")
router.register("register", UserViewset, basename="register")

urlpatterns = [
    path("", include(router.urls))
]
