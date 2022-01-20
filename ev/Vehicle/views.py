from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import Vehicle, Battery, Device, Driver
from .forms import VehicleForm, VehicleUpdateForm, BatteryForm, DeviceForm, DriverForm
from django.urls import reverse_lazy
from .filters import VehicleFilter, BatteryFilter, DriverFilter, DeviceFilter
from ev.permissions import AdminOnlyPermissions
from account.forms import RegistrationForm
from Profile.forms import ProfileDriverForm


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
                organization=self.request.user.profiles.organization)
        context.update({
            "vehicles": vehicles,
            "vehicles_filter": vehicles_filter
        })
        return context


class vehicleCreateView(LoginRequiredMixin, AdminOnlyPermissions,  CreateView):
    template_name = "vehicles/create_vehicle.html"
    form_class = VehicleForm


class VehicleUpdateView(LoginRequiredMixin, AdminOnlyPermissions, UpdateView):
    queryset = Vehicle.objects.all()
    template_name = "vehicles/update_vehicle.html"
    form_class = VehicleUpdateForm
    context_object_name = "vehicle"


class VehicleDeleteView(LoginRequiredMixin, AdminOnlyPermissions, DeleteView):
    queryset = Vehicle.objects.all()
    template_name = "vehicles/delete_vehicle.html"
    context_object_name = "vehicle"
    success_url = reverse_lazy("vehicle-list")


""" Battery """


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


class BatteryCreateView(LoginRequiredMixin, AdminOnlyPermissions, CreateView):
    template_name = "battery/create_battery.html"
    form_class = BatteryForm


class BatteryUpdateView(LoginRequiredMixin, AdminOnlyPermissions, UpdateView):
    queryset = Battery.objects.all()
    template_name = "battery/update_battery.html"
    form_class = BatteryForm
    context_object_name = "battery"


class BatteryDeleteView(LoginRequiredMixin, AdminOnlyPermissions, DeleteView):
    queryset = Battery.objects.all()
    template_name = "battery/delete_battery.html"
    context_object_name = "battery"
    success_url = reverse_lazy("battery-list")


""" Device """


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


class DeviceCreateView(LoginRequiredMixin, AdminOnlyPermissions, CreateView):
    template_name = "device/create_device.html"
    form_class = DeviceForm


class DeviceUpdateView(LoginRequiredMixin, AdminOnlyPermissions, UpdateView):
    queryset = Device.objects.all()
    template_name = "device/update_device.html"
    form_class = DeviceForm
    context_object_name = "device"


class DeviceDeleteView(LoginRequiredMixin, AdminOnlyPermissions, DeleteView):
    queryset = Device.objects.all()
    template_name = "device/delete_device.html"
    context_object_name = "device"
    success_url = reverse_lazy("device-list")


""" Driver """


class DriverListView(LoginRequiredMixin, ListView):
    model = Driver
    template_name = "driver/driver_list.html"
    context_object_name = "drivers"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        drivers_filter = DriverFilter(
            self.request.GET
        )
        drivers = drivers_filter.qs
        if not self.request.user.is_superuser:
            drivers = drivers.filter(
                organization=self.request.user.profiles.organization)
        context.update({
            "drivers": drivers,
            "drivers_filter": drivers_filter
        })
        return context


class DriverCreateView(LoginRequiredMixin, AdminOnlyPermissions, CreateView):
    template_name = "driver/create_driver.html"
    form_class = DriverForm


class DriverUpdateView(LoginRequiredMixin, AdminOnlyPermissions, UpdateView):
    queryset = Driver.objects.all()
    template_name = "driver/update_driver.html"
    form_class = DriverForm
    context_object_name = "driver"


class DriverDeleteView(LoginRequiredMixin, AdminOnlyPermissions, DeleteView):
    queryset = Driver.objects.all()
    template_name = "driver/delete_driver.html"
    context_object_name = "driver"
    success_url = reverse_lazy("driver-list")


def driver_registration_view(request):
    context = {}
    if request.POST:
        form = RegistrationForm(request.POST)

        profile_form = ProfileDriverForm(data=request.POST)
        # print(profile_form.data)
        if form.is_valid() and profile_form.is_valid():
            user = form.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.organization = request.user.profile.organization
            profile.save()
            # email = form.cleaned_data.get('email')
            # password = form.cleaned_data.get("password1")
            # account = authenticate(email=email, password=password)
            # login(request, account)
            return redirect('register')
        else:
            context["registration_form"] = form
            context["profile_form"] = profile_form
    else:
        form = RegistrationForm()
        profile_form = ProfileDriverForm()
        context["registration_form"] = form
        context["profile_form"] = profile_form

    return render(request, "account/register.html", context)
