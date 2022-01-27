from django.http import HttpResponse, HttpResponseForbidden, HttpResponseNotFound, Http404
from django.shortcuts import render
from django.contrib.auth.mixins import PermissionRequiredMixin


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
        elif request.user.profile.profile_type == "manager":
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
        elif self.request.user.profile.profile_type == "manager":
            print("maanager")
            return True
        return False
