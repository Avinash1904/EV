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
from Dashboard.views import map

admin.site.site_header = " "
# admin.site.site_title = "Admin Console"
admin.site.index_title = "Admin Console"
urlpatterns = [
    path('', TemplateView.as_view(template_name='index.html'), name='home'),
    path('main', TemplateView.as_view(template_name='main.html'), name='main'),
    path("vehicles/", include("Vehicle.urls"), name="vehicle"),
    # path('vehicles', TemplateView.as_view(
    #     template_name='vehicles/vehicles_list.html'), name='vehicle_list'),
    path('admin/Dashboard/googlemap/',
         TemplateView.as_view(template_name='admin/live_maps.html'), name='live_map'),
    path('index/', TemplateView.as_view(template_name='index.html'), name='home'),
    path('admin/', admin.site.urls),
    # path('accounts/', include('Profile.urls')),
    # path('accounts/', include('django.contrib.auth.urls')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
