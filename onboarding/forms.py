from django import forms
from .models import ContractorSignupRequest


SERVICE_CATEGORY_CHOICES = [
    ("Concrete", "Concrete"),
    ("Plumbing", "Plumbing"),
    ("Electrical", "Electrical"),
    ("HVAC", "HVAC"),
    ("Roofing", "Roofing"),
    ("Landscaping", "Landscaping"),
    ("Handyman", "Handyman"),
    ("Painting", "Painting"),
    ("Flooring", "Flooring"),
    ("Remodeling", "Remodeling"),
    ("Other", "Other"),
]


class ContractorSignupRequestForm(forms.ModelForm):
    service_categories = forms.MultipleChoiceField(
        choices=SERVICE_CATEGORY_CHOICES,
        required=False,
        widget=forms.CheckboxSelectMultiple,
    )

    # This field is NOT stored directly in the model
    other_service_category = forms.CharField(
        required=False,
        max_length=20,
        label="Other service category",
        widget=forms.TextInput(attrs={
            "placeholder": "Enter custom category",
            "maxlength": 20,
        }),
    )

    class Meta:
        model = ContractorSignupRequest
        fields = [
            "business_name",
            "contact_name",
            "email",
            "phone",
            "service_categories",
            "other_service_category",
            "service_area",
            "licensed_and_insured",
            "license_insurance_notes",
            "best_time_to_contact",
            "website_url",
            "years_in_business",
            "notes",
        ]

        widgets = {
            "service_area": forms.Textarea(attrs={"rows": 3}),
            "license_insurance_notes": forms.Textarea(attrs={"rows": 3}),
            "notes": forms.Textarea(attrs={"rows": 4}),
        }

    def clean(self):
        cleaned = super().clean()
        categories = cleaned.get("service_categories") or []
        other_value = (cleaned.get("other_service_category") or "").strip()

        if "Other" in categories:
            if not other_value:
                raise forms.ValidationError(
                    "Please specify your service category when selecting 'Other'."
                )

            # Replace "Other" with the custom value
            categories = [c for c in categories if c != "Other"]
            categories.append(other_value)

        cleaned["service_categories"] = categories
        return cleaned 