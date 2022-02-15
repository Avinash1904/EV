from django.http import HttpResponse, HttpResponseForbidden, HttpResponseNotFound, Http404
from django.shortcuts import render
from django.contrib.auth.mixins import PermissionRequiredMixin
from Profile.models import Role


def admin_only(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_admin:
            return view_func(request, *args, **kwargs)
        else:
            print("yolo")
            # return HttpResponseNotFound()
            raise Http404()
    return wrapper_func


def admin_or_manager_only(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_admin:
            return view_func(request, *args, **kwargs)
        # elif request.user.profile.profile_type == "manager":
        elif request.user.profile.role == Role.objects.get(id=2):
            return view_func(request, *args, **kwargs)
        else:
            print("yolo1")
            # return HttpResponseNotFound()
            raise Http404()
    return wrapper_func


class AdminOnlyPermissions(PermissionRequiredMixin):
    def has_permission(self):
        if self.request.user.is_admin:
            return True
        return False


class AdminOrManagerOnlyPermissions(PermissionRequiredMixin):
    def has_permission(self):
        if self.request.user.is_admin:
            return True
        # elif self.request.user.profile.profile_type == "manager":
        elif self.request.user.profile.role == Role.objects.get(id=2):
            print("maanager")
            return True
        return False
