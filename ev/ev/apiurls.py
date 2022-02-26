from rest_framework.routers import DefaultRouter
from django.urls import include, path
from Profile.apis.viewsets import ProfileViewset, HomeViewSet
from Vehicle.apis.viewsets import VehicleViewset, BatteryViewset, DeviceViewset, TripViewset, LiveStatusViewset
from account.apis.viewsets import UserViewset

router = DefaultRouter()
router.register("profiles", ProfileViewset, basename="profiles")
router.register("vehicles", VehicleViewset, basename="vehicles")
router.register("battery", BatteryViewset, basename="battery")
router.register("trip", TripViewset, basename="trip")
router.register("register", UserViewset, basename="register")
router.register("home", HomeViewSet, basename="home")
router.register("live-status", LiveStatusViewset, basename="live-status")
urlpatterns = [
    path("", include(router.urls))
]
