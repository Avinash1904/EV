from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import Vehicle, Battery, Device, Driver
from .forms import VehicleForm, VehicleUpdateForm, BatteryForm, DeviceForm, DriverForm
from django.urls import reverse_lazy
from .filters import VehicleFilter, BatteryFilter, DriverFilter, DeviceFilter
from ev.permissions import AdminOnlyPermissions, AdminOrManagerOnlyPermissions, admin_only, admin_or_manager_only
from account.forms import RegistrationForm
from Profile.forms import ProfileDriverForm
from Profile.models import Profile
from dal import autocomplete
from django.http import HttpResponse
from django.utils.decorators import method_decorator


@method_decorator(admin_only, name="dispatch")
class BatteryAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        print("autocomplet ")
        qs = Battery.objects.filter(vehicle=None)
        if self.q:
            qs = qs.filter(battery_number__istartswith=self.q)

        return qs


@method_decorator(admin_only, name="dispatch")
class DeviceAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        print("autocomplet ")
        qs = Device.objects.filter(vehicle=None)
        if self.q:
            qs = qs.filter(imei_number__istartswith=self.q)

        return qs


@method_decorator(admin_or_manager_only, name="dispatch")
class VehicleListView(LoginRequiredMixin, ListView):
    model = Vehicle
    template_name = "vehicles/vehicles_list.html"
    context_object_name = "vehicles"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        vehicles_filter = VehicleFilter(
            self.request.GET
        )
        vehicles = vehicles_filter.qs
        if not self.request.user.is_superuser:
            vehicles = vehicles.filter(
                organization=self.request.user.profile.organization)
        context.update({
            "vehicles": vehicles,
            "vehicles_filter": vehicles_filter
        })
        return context


@method_decorator(admin_only, name="dispatch")
class vehicleCreateView(LoginRequiredMixin, AdminOnlyPermissions,  CreateView):
    template_name = "vehicles/create_vehicle.html"
    form_class = VehicleForm


@method_decorator(admin_only, name="dispatch")
class VehicleUpdateView(LoginRequiredMixin, AdminOnlyPermissions, UpdateView):
    queryset = Vehicle.objects.all()
    template_name = "vehicles/update_vehicle.html"
    form_class = VehicleUpdateForm
    context_object_name = "vehicle"


@method_decorator(admin_only, name="dispatch")
class VehicleDeleteView(LoginRequiredMixin, AdminOnlyPermissions, DeleteView):
    queryset = Vehicle.objects.all()
    template_name = "vehicles/delete_vehicle.html"
    context_object_name = "vehicle"
    success_url = reverse_lazy("vehicle-list")


""" Battery """


@method_decorator(admin_or_manager_only, name="dispatch")
class BatteryListView(LoginRequiredMixin, ListView):
    model = Battery
    template_name = "battery/battery_list.html"
    context_object_name = "batteries"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        batteries_filter = BatteryFilter(
            self.request.GET
        )
        batteries = batteries_filter.qs
        context.update({
            "batteries": batteries,
            "batteries_filter": batteries_filter
        })
        return context


@method_decorator(admin_only, name="dispatch")
class BatteryCreateView(LoginRequiredMixin, AdminOnlyPermissions, CreateView):
    template_name = "battery/create_battery.html"
    form_class = BatteryForm


@method_decorator(admin_only, name="dispatch")
class BatteryUpdateView(LoginRequiredMixin, AdminOnlyPermissions, UpdateView):
    queryset = Battery.objects.all()
    template_name = "battery/update_battery.html"
    form_class = BatteryForm
    context_object_name = "battery"


@method_decorator(admin_only, name="dispatch")
class BatteryDeleteView(LoginRequiredMixin, AdminOnlyPermissions, DeleteView):
    queryset = Battery.objects.all()
    template_name = "battery/delete_battery.html"
    context_object_name = "battery"
    success_url = reverse_lazy("battery-list")


""" Device """


@method_decorator(admin_only, name="dispatch")
class DeviceListView(LoginRequiredMixin, ListView):
    model = Device
    template_name = "device/device_list.html"
    context_object_name = "devices"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        devices_filter = DeviceFilter(
            self.request.GET
        )
        devices = devices_filter.qs
        context.update({
            "devices": devices,
            "devices_filter": devices_filter
        })
        return context


@method_decorator(admin_only, name="dispatch")
class DeviceCreateView(LoginRequiredMixin, AdminOnlyPermissions, CreateView):
    template_name = "device/create_device.html"
    form_class = DeviceForm


@method_decorator(admin_only, name="dispatch")
class DeviceUpdateView(LoginRequiredMixin, AdminOnlyPermissions, UpdateView):
    queryset = Device.objects.all()
    template_name = "device/update_device.html"
    form_class = DeviceForm
    context_object_name = "device"


@method_decorator(admin_only, name="dispatch")
class DeviceDeleteView(LoginRequiredMixin, AdminOnlyPermissions, DeleteView):
    queryset = Device.objects.all()
    template_name = "device/delete_device.html"
    context_object_name = "device"
    success_url = reverse_lazy("device-list")


""" Driver """


@method_decorator(admin_or_manager_only, name="dispatch")
class DriverListView(LoginRequiredMixin, ListView):
    model = Profile
    template_name = "driver/driver_list.html"
    context_object_name = "drivers"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_superuser:
            drivers_filter = DriverFilter(
                self.request.GET, Profile.objects.filter(
                    profile_type="driver")
            )
        else:
            drivers_filter = DriverFilter(
                self.request.GET, Profile.objects.filter(
                    profile_type="driver", organization=self.request.user.profile.organization)
            )
        drivers = drivers_filter.qs
        if not self.request.user.is_superuser:
            drivers = drivers.filter(
                organization=self.request.user.profile.organization)
        context.update({
            "drivers": drivers,
            "drivers_filter": drivers_filter
        })
        return context


@method_decorator(admin_or_manager_only, name="dispatch")
class DriverUpdateView(LoginRequiredMixin, UpdateView):
    queryset = Profile.objects.all()
    template_name = "driver/update_driver.html"
    form_class = ProfileDriverForm
    context_object_name = "driver"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = self.get_object()
        assigned_vehicles = profile.vehicles.all()
        available_vehicles = None
        try:
            available_vehicles = profile.organization.vehicles.all().filter(profile=None)
        except Exception:
            available_vehicles = Vehicle.objects.filter(
                profile=None, organization=None)

        context.update({
            "assigned_vehicles": assigned_vehicles,
            "available_vehicles": available_vehicles
        })
        return context

    def form_invalid(self, form):
        print("invalid form ", form.data)
        return HttpResponse("Invalid")

    def form_valid(self, form):
        print("valid form ", form.data)
        req = form.data.get("button", None)
        print("req is ", req)
        driver = form.save(commit=False)
        if req == "remove":
            driver.vehicles.clear()
            driver.organization = None
            driver.save()
        elif req == "update":
            driver.save()
            vehicles = self.request.POST.getlist("vehicles", None)
            driver.vehicles.clear()
            for vehicle in vehicles:
                driver.vehicles.add(Vehicle.objects.get(id=vehicle))

        elif req == "accept":
            print("driver is ", driver)
            driver.document_verification_status = Profile.ACCEPTED
            driver.save()

        elif req == "pending":
            driver.document_verification_status = Profile.PENDING
            driver.save()
            driver.vehicles.clear()

        elif req == "reject":
            driver.document_verification_status = Profile.REJECTED
            driver.save()
            driver.vehicles.clear()

        return super().form_valid(form)

    def get_success_url(self):
        return reverse("driver-list")


@method_decorator(admin_only, name="dispatch")
class DriverDeleteView(LoginRequiredMixin, AdminOnlyPermissions, DeleteView):
    queryset = Driver.objects.all()
    template_name = "driver/delete_driver.html"
    context_object_name = "driver"
    success_url = reverse_lazy("driver-list")


@admin_or_manager_only
def driver_registration_view(request):
    print("driver creation .. ")
    context = {}
    if request.POST:
        form = RegistrationForm(request.POST)

        profile_form = ProfileDriverForm(data=request.POST)
        # print(profile_form.data)
        if form.is_valid() and profile_form.is_valid():
            user = form.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            if not request.user.is_superuser:
                profile.organization = request.user.profile.organization
            profile.save()
            return redirect('driver-create')
        else:
            context["registration_form"] = form
            context["profile_form"] = profile_form
    else:
        print("else")
        form = RegistrationForm()
        profile_form = ProfileDriverForm()
        context["registration_form"] = form
        context["profile_form"] = profile_form

    return render(request, "driver/create_driver.html", context)
