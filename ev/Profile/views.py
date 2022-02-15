from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from ev.permissions import AdminOnlyPermissions, admin_only, admin_or_manager_only
from .models import Profile
from .filters import ProfileFilter
from .forms import ProfileForm
from Vehicle.models import Vehicle
from django.utils.decorators import method_decorator


@method_decorator(admin_only, name="dispatch")
class ProfileListView(ListView):
    model = Profile
    template_name = "profile/profile_list.html"
    context_object_name = "profiles"

    def get_queryset(self):
        # profile_type = self.request.GET.get("profile_type", None)
        # if profile_type == "manager" or profile_type == "driver":
        #     return Profile.objects.filter(profile_type=profile_type)
        return Profile.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profiles_filter = ProfileFilter(self.request.GET, self.get_queryset())
        context.update({
            "profiles_filter": profiles_filter
        })
        return context


@method_decorator(admin_only, name="dispatch")
class ProfileUpdateView(LoginRequiredMixin, AdminOnlyPermissions, UpdateView):
    queryset = Profile.objects.all()
    template_name = "profile/update_profile.html"
    form_class = ProfileForm
    context_object_name = "profile"

    def get_success_url(self):
        return reverse("profile-list")


@method_decorator(admin_only, name="dispatch")
class ProfileDeleteView(LoginRequiredMixin, AdminOnlyPermissions, DeleteView):
    queryset = Profile.objects.all()
    template_name = "profile/delete_profile.html"
    context_object_name = "profile"
    success_url = reverse_lazy("profile-list")
