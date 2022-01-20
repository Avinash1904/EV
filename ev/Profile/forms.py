from django import forms
from .models import Profile


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ("first_name", "last_name", "uid",
                  "organization", "profile_type")


class ProfileDriverForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ("first_name", "last_name", "uid")


# class ManagerUpdateForm(forms.ModelForm):
#     class Meta:
#         model = Profile
#         fields = ("first_name", "last_name", "uid", "vehicle")
