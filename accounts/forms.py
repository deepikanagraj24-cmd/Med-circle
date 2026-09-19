from django import forms
from .models import Doctor


class DoctorRegistrationForm(forms.ModelForm):

    class Meta:

        model = Doctor

        fields = [
            "full_name",
            "email",
            "phone_number",
            "specialization",
            "qualification",
            "medical_registration_number",
            "password",
        ]

        widgets = {
            "password": forms.PasswordInput()
        }