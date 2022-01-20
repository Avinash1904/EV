from django.urls import path
from .views import ReportView, report_view

urlpatterns = [
    path("", report_view, name="reports")
]
