from django.urls import path 
from .views import homepage
from .views import cleaning

urlpatterns = [
    path("", homepage, name = "homepage"),
    path("cleaning/", cleaning, name = "cleaning"  )
]