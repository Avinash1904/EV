from django.urls import path
from .views import ProfileListView, ProfileUpdateView, ProfileDeleteView

urlpatterns = [
    path('', ProfileListView.as_view(), name='profile-list'),
    path('<pk>/update/', ProfileUpdateView.as_view(), name='profile-update'),
    path('<pk>/delete/', ProfileDeleteView.as_view(), name='profile-delete'),
]
