from django.shortcuts import render
from django.contrib.auth.decorators import login_required

def contractor_login(request):
    return render(request, "contractorportal/contractor_login.html")

@login_required
def dashboard(request):
    return render(request, "contractorportal/dashboard.html")

