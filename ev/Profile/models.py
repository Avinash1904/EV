from django.db import models
from account.models import Account
from account.models import Organization


class Role(models.Model):
    name = models.CharField(max_length=50, default="user")

    def __str__(self):
        return self.name


class Profile(models.Model):
    DRIVER = "driver"
    MANAGER = "manager"
    PROFILE_CHOICES = (
        (DRIVER, "Driver"),
        (MANAGER, "Manager")
    )

    ACCEPTED = "accepted"
    REJECTED = "rejected"
    PENDING = "pending"

    DOCUMENT_VERIFICATION_STATUS_CHOICES = (
        (ACCEPTED, "Accepted"),
        (REJECTED, "Rejected"),
        (PENDING, "Pending")
    )

    user = models.OneToOneField(
        Account, on_delete=models.CASCADE, related_name="profile")
    first_name = models.CharField(max_length=50, verbose_name="first name")
    last_name = models.CharField(max_length=50, verbose_name="last name")
    ktp_number = models.CharField(
        max_length=100, verbose_name="KTP Number")
    profile_type = models.CharField(
        max_length=100, verbose_name="Profile Type",
        choices=PROFILE_CHOICES, default=DRIVER
        )
    role = models.ForeignKey(Role, related_name="profile",
                             on_delete=models.SET_NULL, blank=True, null=True)
    ktp_image = models.ImageField(
        default="ktp/bg2.png", null=True, blank=True, upload_to="ktp")
    sim_image = models.ImageField(
        default="ktp/bg2.png", null=True, blank=True, upload_to="sim")
    document_verification_status = models.CharField(
        max_length=100,
        choices=DOCUMENT_VERIFICATION_STATUS_CHOICES,
        default=PENDING,
        verbose_name="Verification Status"
    )
    organization = models.ForeignKey(
        Organization, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return (self.first_name + ' ' + self.profile_type)
