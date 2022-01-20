from django.urls import path
from .views import (registration_view, logout_view, login_view, OrganizationCreateView, OrganizationListView, OrganizationUpdateView,
                    change_password)
urlpatterns = [
    path("register/", registration_view, name="register"),
    path("logout/", logout_view, name="logout"),
    path("login/", login_view, name="login1"),
    path("organization/create", OrganizationCreateView.as_view(),
         name="organization-create"),
    path("organizations/", OrganizationListView.as_view(),
         name="organization-list"),
    path("organizations/<pk>/update/", OrganizationUpdateView.as_view(),
         name="organization-update"),
    path("password-change/", change_password, name="password-change"),
]
