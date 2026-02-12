from django.conf import settings
from django.db import models


class ContractorSignupRequest(models.Model):
    class Status(models.TextChoices):
        NEW = "NEW", "New"
        CONTACTED = "CONTACTED", "Contacted"
        APPROVED = "APPROVED", "Approved"
        REJECTED = "REJECTED", "Rejected"

    business_name = models.CharField(max_length=200)
    contact_name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=50)

    # Store selected categories as JSON array of strings (e.g. ["Concrete", "Plumbing"])
    service_categories = models.JSONField(default=list, blank=True)

    # Free-form coverage area (cities/ZIPs)
    service_area = models.TextField(help_text="Cities, neighborhoods, ZIP codes you serve")

    # Checkbox + notes
    licensed_and_insured = models.BooleanField(default=False)
    license_insurance_notes = models.TextField(blank=True)

    best_time_to_contact = models.CharField(max_length=200, blank=True)
    notes = models.TextField(blank=True)

    # Optional extras (from the earlier “optional” list, excluding “referral source”)
    website_url = models.URLField(blank=True)
    years_in_business = models.PositiveIntegerField(null=True, blank=True)

    status = models.CharField(max_length=20, choices=Status.choices, default=Status.NEW)

    created_at = models.DateTimeField(auto_now_add=True)

    # Nullable USer Foreign Key to link signup requests to created users
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="signup_request",
    ) 

    def __str__(self) -> str:
        return f"{self.business_name} ({self.contact_name}) - {self.created_at:%Y-%m-%d}" 
