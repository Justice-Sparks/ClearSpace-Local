# onboarding/admin.py
from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.urls import reverse

from .models import ContractorSignupRequest
from contractorportal.models import ContractorProfile

User = get_user_model()


@admin.register(ContractorSignupRequest)
class ContractorSignupRequestAdmin(admin.ModelAdmin):
    list_display = ("business_name", "contact_name", "email", "status", "created_at")
    list_filter = ("status", "created_at")
    search_fields = ("business_name", "contact_name", "email", "phone")
    actions = ["approve_and_create_account", "mark_contacted", "mark_rejected"]

    @admin.action(description="Approve + create contractor account + email password setup link")
    def approve_and_create_account(self, request, queryset):
        for app in queryset:
            if app.status == ContractorSignupRequest.Status.APPROVED and app.user_id:
                continue

            # Create or fetch user by email
            user, created = User.objects.get_or_create(
                email=app.email,
                defaults={
                    "username": app.email,  # keep it simple
                    "first_name": app.contact_name.split(" ")[0] if app.contact_name else "",
                    "is_active": True,
                },
            )

            if created:
                user.set_unusable_password()
                user.save()

            # Create contractor profile
            ContractorProfile.objects.get_or_create(
                user=user,
                defaults={
                    "business_name": app.business_name,
                    "contact_name": app.contact_name,
                    "phone": app.phone,
                },
            )

            # Link request → user, update status
            app.user = user
            app.status = ContractorSignupRequest.Status.APPROVED
            app.save(update_fields=["user", "status"])

            # Email password set link
            uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)

            # This URL name comes from django auth password reset confirm
            path = reverse("password_reset_confirm", kwargs={"uidb64": uidb64, "token": token})
            domain = request.get_host()
            reset_link = f"https://{domain}{path}"

            subject = "You’ve been approved — set your password"
            message = (
                f"Hi {app.contact_name or ''},\n\n"
                f"Your contractor account has been approved.\n"
                f"Set your password here:\n{reset_link}\n\n"
                f"If you didn’t request this, you can ignore this email."
            )

            send_mail(subject, message, None, [user.email], fail_silently=False)

    @admin.action(description="Mark as contacted")
    def mark_contacted(self, request, queryset):
        queryset.update(status=ContractorSignupRequest.Status.CONTACTED)

    @admin.action(description="Mark as rejected")
    def mark_rejected(self, request, queryset):
        queryset.update(status=ContractorSignupRequest.Status.REJECTED) 