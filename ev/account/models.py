from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from uuid import uuid4
from django.urls import reverse


class UUIDManager(models.Manager):
    def get_by_natural_key(self, uuid):
        return self.get(uuid=uuid)


class UUIDModel(models.Model):
    uuid = models.UUIDField(
        default=uuid4, unique=True, editable=False, verbose_name="UUID"
    )
    objects = UUIDManager()

    class Meta:
        abstract = True

    def natural_key(self):
        return self.uuid


class MyAccountManager(BaseUserManager):
    def create_user(self, email, password=None):
        if not email:
            raise ValueError("Users must have an email address")

        user = self.model(email=self.normalize_email(email))

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        user = self.create_user(email=email, password=password)

        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class Account(AbstractBaseUser):
    email = models.EmailField(verbose_name="email",
                              max_length=100, unique=True, blank=True, null=True)
    phone_number = models.CharField(
        max_length=15, unique=True, blank=True, null=True)
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="created at")
    date_joined = models.DateTimeField(
        auto_now=True, verbose_name="Date Joined")
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_password_changed = models.BooleanField(default=False)
    firebase_uid = models.CharField(
        unique=True, null=True, blank=True, max_length=100)
    country_code = models.CharField(
        max_length=5, null=True, blank=True, verbose_name="Country Code")

    USERNAME_FIELD = 'email'
    objects = MyAccountManager()

    def __str__(self):
        return self.email or self.phone_number

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True


class Organization(UUIDModel):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('organization-list')
