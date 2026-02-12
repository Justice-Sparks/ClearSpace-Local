from django.urls import path
from .views import contractor_login, dashboard, portal_redirect

urlpatterns = [
    #path("contractors/login/", contractor_login, name="contractor_login"),
    path("", dashboard, name="contractor_dashboard"),
] 