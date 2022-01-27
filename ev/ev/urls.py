"""ev URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import TemplateView
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

admin.site.site_header = " "
# admin.site.site_title = "Admin Console"
admin.site.index_title = "Admin Console"
urlpatterns = [
    path('', TemplateView.as_view(template_name='base/index.html'), name='home'),
    path("vehicles/", include("Vehicle.urls"), name="vehicle"),
    path('dashboard/', include("Dashboard.urls"), name='dashboard'),
    path('report/', include("Report.urls"), name='report'),
    path('alert/', include("Alert.urls"), name='alert'),
    path('admin/', admin.site.urls),
    path("accounts/", include("account.urls"), name="account"),
    path("profiles/", include("Profile.urls"), name="profile"),
    path("password-change/", auth_views.PasswordChangeView.as_view(
        template_name="account/password_change.html"), name="password_change"),
    path("password-change-done/", auth_views.PasswordChangeDoneView.as_view(
        template_name="account/password_change_complete.html"), name="password_change_complete"),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
