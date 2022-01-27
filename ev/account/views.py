from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from .forms import RegistrationForm, AccountAuthenticationForm, OrganizationCreateForm, OrganizationUpdateForm
from ev.permissions import admin_only
from django.contrib.auth.decorators import login_required
from Profile.forms import ProfileForm
from Profile.models import Profile
from .models import Organization
from django.views.generic import CreateView, ListView, UpdateView
from Vehicle.models import Vehicle
from .filters import OrganizationFilter
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from ev.permissions import AdminOnlyPermissions, admin_only
from django.utils.decorators import method_decorator


@admin_only
def registration_view(request):
    context = {}
    if request.POST:
        form = RegistrationForm(request.POST)

        profile_form = ProfileForm(data=request.POST)
        print("profile form ", profile_form.data)
        # print(profile_form.data)
        if form.is_valid() and profile_form.is_valid():
            print("yoooo")
            user = form.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            print(profile.user)
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
        profile_form = ProfileForm()
        context["registration_form"] = form
        context["profile_form"] = profile_form

    return render(request, "account/register.html", context)


@login_required
def logout_view(request):
    logout(request)
    return redirect("login1")


def login_view(request):
    context = {}
    user = request.user
    if user.is_authenticated:
        return redirect("vehicle-list")

    if request.POST:
        form = AccountAuthenticationForm(request.POST)
        if form.is_valid:
            email = request.POST["email"]
            password = request.POST["password"]
            user = authenticate(email=email, password=password)
            if user:
                login(request, user)
                if user.is_password_changed:
                    return redirect("vehicle-list")

                return redirect("password-change")
    else:
        form = AccountAuthenticationForm()

    context["login_form"] = form
    return render(request, "account/login.html", context)


@login_required
def change_password(request):
    if request.POST:
        form = PasswordChangeForm(request.user, request.POST)
        print("form data ", form.data)
        print("usr ", request.user)
        if form.is_valid():
            print("valid")
            user = form.save()
            user.is_password_changed = True
            user.save()
            return redirect("login1")

    form = PasswordChangeForm(request.user)
    return render(request, "account/password_change.html", {"form": form})


@method_decorator(admin_only, name="dispatch")
class OrganizationCreateView(AdminOnlyPermissions, CreateView):
    form_class = OrganizationCreateForm
    template_name = "account/organization_create.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        available_vehicles = Vehicle.objects.filter(organization=None)
        context.update({
            "available_vehicles": available_vehicles,
        })
        return context

    def form_valid(self, form):
        print(form.cleaned_data)
        vehicles = form.cleaned_data.get("available_vehicles", None)
        org = form.save()
        if vehicles:
            for vehicle in vehicles:
                org.vehicles.add(vehicle)
        return super().form_valid(form)


@method_decorator(admin_only, name="dispatch")
class OrganizationListView(AdminOnlyPermissions, ListView):
    model = Organization
    template_name = "account/organization_list.html"
    context_object_name = "organizations"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        organizations_filter = OrganizationFilter(
            self.request.GET
        )
        organizations = organizations_filter.qs
        context.update({
            "organizations": organizations,
            "organizations_filter": organizations_filter
        })
        return context


@method_decorator(admin_only, name="dispatch")
class OrganizationUpdateView(AdminOnlyPermissions, UpdateView):
    queryset = Organization.objects.all()
    template_name = "account/update_organization.html"
    form_class = OrganizationUpdateForm
    context_object_name = "organization"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        org = self.get_object()
        selected_vehicles = org.vehicles.all()
        available_vehicles = Vehicle.objects.filter(organization=None)
        context.update({
            "available_vehicles": available_vehicles,
            "selected_vehicles": selected_vehicles,
        })
        return context

    def form_valid(self, form):
        org = form.save()
        vehicles = self.request.POST.getlist("vehicles", None)
        if vehicles:
            for vehicle in vehicles:
                org.vehicles.add(Vehicle.objects.get(id=vehicle))
        else:
            org.vehicles.clear()
        return super().form_valid(form)
