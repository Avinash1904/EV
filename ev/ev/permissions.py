from django.http import HttpResponse
from django.shortcuts import redirect
from django.contrib.auth.mixins import PermissionRequiredMixin


def admin_only(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_admin:
            return view_func(request, *args, **kwargs)
        else:
            return HttpResponse("You are not authorized to perform this action")
    return wrapper_func


class AdminOnlyPermissions(PermissionRequiredMixin):
    def has_permission(self):
        return self.request.user.is_admin
