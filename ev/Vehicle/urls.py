
from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import TemplateView
from django.conf import settings
from django.conf.urls.static import static
from .views import VehicleListView, vehicleCreateView, VehicleUpdateView, VehicleDeleteView

admin.site.site_header = " "
# admin.site.site_title = "Admin Console"
admin.site.index_title = "Admin Console"
urlpatterns = [
    path('', VehicleListView.as_view(), name='vehicle-list'),
    path('create/', vehicleCreateView.as_view(), name='vehicle-create'),
    path('<pk>/update/', VehicleUpdateView.as_view(), name='vehicle-update'),
    path('<pk>/delete/', VehicleDeleteView.as_view(), name='vehicle-delete'),
]
