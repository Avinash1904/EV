from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Account, Organization
from Vehicle.models import Vehicle
from django.contrib.auth import authenticate


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(
        max_length=100, help_text="Required. Add a valid email address.")

    class Meta:
        model = Account
        fields = ("email", "password1", "password2")


class AccountAuthenticationForm(forms.ModelForm):
    password = forms.CharField(label="Password", widget=forms.PasswordInput)

    class Meta:
        model = Account
        fields = ("email", "password")

    def clean(self):
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")

        if not authenticate(email=email, password=password):
            raise forms.ValidationError("Invalid Login")


class OrganizationCreateForm(forms.ModelForm):
    # available_vehicles = forms.ModelMultipleChoiceField(
    #     widget=forms.CheckboxSelectMultiple(),
    #     queryset=Vehicle.objects.filter(organization=None))

    class Meta:
        model = Organization
        fields = ("name",)


class OrganizationUpdateForm(forms.ModelForm):
    class Meta:
        model = Organization
        fields = ("name",)
