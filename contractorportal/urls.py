from django.urls import path
from .views import dashboard

urlpatterns = [
    path("contractor/dashboard/", dashboard, name="contractor_dashboard"),
]