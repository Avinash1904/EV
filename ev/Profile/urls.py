from django.urls import path
from .views import SignUpView, login_request, logout_request

urlpatterns = [
    #path('signup/', SignUpView.as_view(), name='signup'),
    path('login/', login_request, name='login'),
    path('logout/', logout_request, name='logout'),
]
