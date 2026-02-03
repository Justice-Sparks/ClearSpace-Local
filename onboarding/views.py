from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods

from .forms import ContractorSignupRequestForm


@require_http_methods(["GET", "POST"])
def contractor_signup_request(request):
    if request.method == "POST":
        form = ContractorSignupRequestForm(request.POST)
        if form.is_valid():
            obj = form.save()

            subject = f"New Contractor Signup Request: {obj.business_name}"
            categories = ", ".join(obj.service_categories or []) or "(none selected)"

            body = "\n".join([
                "A new contractor signup request was submitted:",
                "",
                f"Business name: {obj.business_name}",
                f"Contact name: {obj.contact_name}",
                f"Email: {obj.email}",
                f"Phone: {obj.phone}",
                f"Service categories: {categories}",
                f"Service area: {obj.service_area}",
                f"Licensed & insured: {'Yes' if obj.licensed_and_insured else 'No'}",
                f"License/insurance notes: {obj.license_insurance_notes or '(none)'}",
                f"Best time to contact: {obj.best_time_to_contact or '(not provided)'}",
                f"Website: {obj.website_url or '(not provided)'}",
                f"Years in business: {obj.years_in_business if obj.years_in_business is not None else '(not provided)'}",
                f"Notes: {obj.notes or '(none)'}",
                "",
                f"Submitted at: {obj.created_at}",
            ])

            send_mail(
                subject=subject,
                message=body,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=settings.CONTRACTOR_SIGNUP_NOTIFY_EMAILS,
                fail_silently=False,
            )

            return redirect("contractor_signup_thanks")
    else:
        form = ContractorSignupRequestForm()

    return render(request, "onboarding/contractor_signup.html", {"form": form})


def contractor_signup_thanks(request):
    return render(request, "onboarding/contractor_signup_thanks.html") 