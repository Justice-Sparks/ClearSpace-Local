
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Django auth: login/logout/password reset flows
    path("accounts/", include("django.contrib.auth.urls")),
    
    # My Apps 
    path("", include("marketplace.urls") ),
    path("onboarding/", include("onboarding.urls") ),
    path("contractor/", include("contractorportal.urls") ),
]

