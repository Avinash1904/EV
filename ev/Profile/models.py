from django.db import models
from account.models import Account
from django.db.models.signals import post_save
from account.models import Organization


class Profile(models.Model):
    DRIVER = "driver"
    MANAGER = "manager"
    PROFILE_CHOICES = (
        (DRIVER, "Driver"),
        (MANAGER, "Manager")
    )
    user = models.OneToOneField(
        Account, on_delete=models.CASCADE, related_name="profiles")
    first_name = models.CharField(max_length=50, verbose_name="first name")
    last_name = models.CharField(max_length=50, verbose_name="last name")
    uid = models.CharField(max_length=100, verbose_name="Unique ID Number")
    profile_type = models.CharField(
        max_length=100, verbose_name="Profile Type",
        choices=PROFILE_CHOICES, default=DRIVER
        )
    organization = models.ForeignKey(
        Organization, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return (self.first_name + ' ' + self.profile_type)


# def post_save_profile_receiver(sender, instance, created, *args, **kwargs):
#     if created:
#
