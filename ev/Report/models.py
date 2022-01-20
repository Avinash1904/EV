from django.db import models

# Create your models here.


class Report2(models.Model):
    start_date = models.DateField()
    end_date = models.DateField()
    report_csv = models.FileField(
        null=True, blank=True, default=None, upload_to='reports', unique=True)


# class Report(models.Model):
#     startlat = models.CharField(max_length=100)
#     firsttime = models.CharField(max_length=100)
#     totaltimevehicleidlesec = models.IntegerField()
#     fuelconsumedgal = models.CharField(max_length=100)
#     endlong = models.CharField(max_length=100)
#     idlepercent = models.IntegerField()
#     totalkm = models.CharField(max_length=100)
#     nighttimedrive = models.CharField(max_length=100)
#     driverlastname = models.CharField(max_length=100)
#     fuelconsumedl = models.CharField(max_length=100)
#     runningpercent = models.CharField(max_length=100)
#     totalmiles = models.CharField(max_length=100)
#     lasttime = models.CharField(max_length=100)
#     endlat = models.CharField(max_length=100)
#     driverfirstname = models.CharField(max_length=100)
#     fuelefficiencykpl = models.CharField(max_length=100)
#     totaltimesegmentsec = models.IntegerField()
#     vehicleuid = models.CharField(max_length=100)
#     totaltimevehiclemovingsec = models.CharField(max_length=100)
#     _id = models.CharField(max_length=200)
#     vehiclesclid = models.CharField(max_length=200)
#     startlong = models.CharField(max_length=100)
#     fuelefficiencympg = models.CharField(max_length=100)
#     created_at = models.DateTimeField(auto_now=True)
#     start_date = models.DateField()
#     end_date = models.DateField()
