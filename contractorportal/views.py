from django.shortcuts import render
from django.contrib.auth.decorators import login_required

def contractor_login(request):
    return render(request, "registration/login.html")

def portal_redirect(request):
    return render(request, "registration/portal_redirect.html")

@login_required
def dashboard(request):
    return render(request, "contractorportal/dashboard.html")

