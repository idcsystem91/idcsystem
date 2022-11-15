from django.urls import path
from .views import ProfileCreateView, ProfileUpdateView

urlpatterns = [
    path("create_profile/", ProfileCreateView.as_view(), name="create_profile"),
    path("<int:pk>/update_profile/",
         ProfileUpdateView.as_view(), name="update_profile"),
]
