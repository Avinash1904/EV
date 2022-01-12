from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import Vehicle
from .forms import VehicleForm, VehicleUpdateForm
from django.urls import reverse_lazy
from .filters import VehicleFilter


class VehicleListView(ListView):
    model = Vehicle
    template_name = "vehicles/vehicles_list.html"
    context_object_name = "vehicles"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        vehicles_filter = VehicleFilter(
            self.request.GET
        )
        vehicles = vehicles_filter.qs
        context.update({
            "vehicles": vehicles,
            "vehicles_filter": vehicles_filter
        })
        return context


class vehicleCreateView(CreateView):
    template_name = "vehicles/create_vehicle.html"
    form_class = VehicleForm


class VehicleUpdateView(UpdateView):
    queryset = Vehicle.objects.all()
    template_name = "vehicles/update_vehicle.html"
    form_class = VehicleUpdateForm
    context_object_name = "vehicle"


class VehicleDeleteView(DeleteView):
    queryset = Vehicle.objects.all()
    template_name = "vehicles/delete_vehicle.html"
    context_object_name = "vehicle"
    success_url = reverse_lazy("vehicle-list")
