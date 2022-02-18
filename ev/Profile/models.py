from django.db import models
from account.models import Account, Organization, UUIDModel
from ev.helpers import get_image_upload_path
from ev.storages import ProfilePicStorageS3, KtpStorageS3, SimStorageS3


class Role(UUIDModel):
    name = models.CharField(max_length=50, default="user")

    def __str__(self):
        return self.name


class Profile(UUIDModel):
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
    ktp_number = models.CharField(blank=True, null=True,
                                  max_length=100, verbose_name="KTP Number")
    sim_number = models.CharField(blank=True, null=True,
                                  max_length=100, verbose_name="SIM Number")
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
    address = models.TextField(null=True, blank=True, verbose_name="Address")
    profile_picture = models.ImageField(
        null=True,
        blank=True,
        upload_to=get_image_upload_path,
        storage=ProfilePicStorageS3()
    )

    def __str__(self):
        return (self.first_name + ' ' + self.profile_type)
