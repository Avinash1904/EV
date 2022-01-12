from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from .models import User
from .forms import UserAdminCreationForm
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate, logout
# Create your views here.


class SignUpView(CreateView):
    form_class = UserAdminCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'


def login_request(request):
    if request.method == "POST":
        print("inside login")
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            print("valid form")
            email = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            print("email ", email)
            user = authenticate(email=email, password=password)
            if user:
                login(request, user)
                return redirect("live")
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    form = AuthenticationForm()
    return render(request, template_name="profile/login.html", context={"login_form": form})


def logout_request(request):
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return redirect("login")
