from django.urls import path
from .views import contractor_login

urlpatterns = [
    path("contractors/login/", contractor_login, name="contractor_login"),
] 