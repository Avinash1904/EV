
from django.urls import path
from .views import map

urlpatterns = [
    path('live/', map, name='live'),
]
