from django.contrib import admin
from .models import ContractorSignupRequest

@admin.register(ContractorSignupRequest)
class ContractorSignupRequestAdmin(admin.ModelAdmin):
    list_display = ("business_name", "contact_name", "email", "phone", "status", "created_at")
    list_filter = ("status", "created_at")
    search_fields = ("business_name", "contact_name", "email", "phone") 
