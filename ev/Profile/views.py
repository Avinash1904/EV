from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from .models import User
from .forms import UserAdminCreationForm
# Create your views here.

class SignUpView(CreateView):
    form_class = UserAdminCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'