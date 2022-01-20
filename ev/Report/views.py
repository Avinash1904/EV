from django.shortcuts import render
from django.http import HttpResponse
import csv
import json
from .models import Report2
from django.views.generic import ListView
from .forms import ReportForm, ReportListForm
import requests
from django.conf import settings
from django.core.files.base import File
import os
from django.contrib.auth.decorators import login_required


@login_required
def report_view(request):
    context = {}
    form = ReportForm(request.POST or None)
    if form.is_valid():
        print(form.cleaned_data.get("start_date"))
        start_date = form.cleaned_data.get("start_date")
        end_date = form.cleaned_data.get("end_date")
        # check if data already exists
        try:
            report = Report2.objects.get(
                start_date=start_date, end_date=end_date)
            file_path = os.path.join(
                settings.MEDIA_ROOT, report.report_csv.path)
            with open(file_path, 'rb') as fh:
                response = HttpResponse(
                    fh.read(), content_type="text/csv")
                response['Content-Disposition'] = 'attachment;filename=' + \
                    os.path.basename(file_path)
                return response

        except Report2.DoesNotExist:
            # convert them in epoch, run the api to get the report, save the data in model and make csv
            login_url = "https://api-aertrakasia.aeris.com/login"
            login_data = {
                "username": "aeris.krish+rentalbanaran@gmail.com", "password": "Selis@123"}
            response = requests.post(login_url, data=login_data)
            if response.status_code == 200:
                access_token = response.json()["access_token"]

                report_url = "https://api-aertrakasia.aeris.com/api/things/data/assets/trips"
                headers = {"token": access_token}
                params = {
                    "startDate": start_date,
                    "endDate": end_date
                }
                report = requests.get(
                    report_url, headers=headers, params=params)
                data_file = open('media/reports2/'+str(start_date)
                                 + '_'+str(end_date)+'.csv', 'w')
                csv_writer = csv.writer(data_file)
                count = 0
                for rep in report.json():
                    if count == 0:
                        header = rep.keys()
                        csv_writer.writerow(header)
                        count += 1
                    csv_writer.writerow(rep.values())
                data_file.close()
                data_file = open('media/reports2/'+str(start_date)
                                 + '_'+str(end_date)+'.csv', 'r')
                report = Report2.objects.create(start_date=start_date,
                                                end_date=end_date, report_csv=File(data_file))
                data_file.close()
                file_path = os.path.join(
                    settings.MEDIA_ROOT, report.report_csv.path)
                with open(file_path, 'rb') as fh:
                    response = HttpResponse(
                        fh.read(), content_type="text/csv")
                    response['Content-Disposition'] = 'attachment;filename=' + \
                        os.path.basename(file_path)
                    return response

                    # repo = Report(**rep)
    context['form'] = form
    reports = Report2.objects.all().order_by("-start_date")
    context["reports"] = reports
    return render(request, "report/list_report.html", context)


class ReportView(ListView):
    model = Report2
    form_class = ReportForm
    template_name = "report/list_report.html"
    context_object_name = "reports"
