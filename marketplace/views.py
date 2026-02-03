from django.shortcuts import render
from .models import City, ServiceCategory

def homepage(request):
    cities = City.objects.all()
    categories = ServiceCategory.objects.all()

    context= {
        "cities" : cities,
        "categories" : categories, 
    }

    return render(request, "homepage.html", context)


def about(request):
    return render(request, "about.html")

def contact(request):
    return render(request, "contact.html")

def cleaning(request):
    return render(request, "residentialcleaning.html")

def contractorportal(request):
    return render(request, "contractorportal.html")

