from django import forms
from .models import Profile


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ("first_name", "last_name", "ktp_number", "role", "address", "profile_picture", "phone_number",
                  "organization", )


class ProfileDriverForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ("first_name", "last_name", "ktp_number", "sim_number", "organization",
                  "sim_image", "ktp_image", "document_verification_status",)
