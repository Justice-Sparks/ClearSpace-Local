from django.urls import path 
from .views import homepage
from .views import cleaning
from .views import contractorportal
from .views import contact
from .views import about


urlpatterns = [
    path("", homepage, name = "homepage"),
    path("about/", about, name = "about"),
    path("contact/", contact, name = "contact"),
    path("cleaning/", cleaning, name = "cleaning" ),
    path("contractorportal/", contractorportal, name = "contractor portal")
]