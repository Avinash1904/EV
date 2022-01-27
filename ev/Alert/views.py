from django.shortcuts import render
from django.http import HttpResponse
import csv
import json
import time
import datetime
from ev.permissions import AdminOrManagerOnlyPermissions, admin_or_manager_only
from django.views.generic import ListView, TemplateView

import requests
from django.conf import settings
from django.core.files.base import File
import os
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


@method_decorator(admin_or_manager_only, name="dispatch")
class AlertView(AdminOrManagerOnlyPermissions, TemplateView):
    template_name = "alert/list_alert.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        login_url = "https://api-aertrakasia.aeris.com/login"
        login_data = {
            "username": "aeris.krish+Rentalbanaran@gmail.com", "password": "Selis@123"}
        response = requests.post(login_url, data=login_data)
        if response.status_code == 200:
            access_token = response.json()["access_token"]

            alert_url = "https://api-aertrakasia.aeris.com/api/fleet/vehicles/alerts"
            headers = {"token": access_token}
            params = {
                "createdAfter": int(datetime.datetime.now().replace(hour=0, minute=0, second=0, microsecond=0).timestamp())*10**3,
                "createdBefore": int(time.time())*10**3
            }
            # hardcoding the time as of now
            # params['createdAfter'] = 1643003083000
            # params['createdBefore'] = 1643089483000

            alert = requests.get(
                alert_url, headers=headers, params=params)

            alerts = []
            #print("alert json ", alert.json())
            if alert.status_code == 200:
                for key, value in alert.json().items():

                    for data in value:
                        alerts.append(data)
            context.update({
                "data": alerts
            })
        return context
