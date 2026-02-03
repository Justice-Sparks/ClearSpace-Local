from django.urls import path
from .views import contractor_signup_request, contractor_signup_thanks

urlpatterns = [
    path("contractors/apply/", contractor_signup_request, name="contractor_signup"),
    path("contractors/apply/thanks/", contractor_signup_thanks, name="contractor_signup_thanks"),
] 