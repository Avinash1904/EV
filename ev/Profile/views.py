from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView
from .models import Profile


class ProfileListView(ListView):
    model = Profile
    template_name = "profile/profile_list.html"
    context_object_name = "profiles"

    def get_queryset(self):
        profile_type = self.request.GET.get("profile_type", None)
        if profile_type == "manager" or profile_type == "driver":
            return Profile.objects.filter(profile_type=profile_type)
        return Profile.objects.all()
