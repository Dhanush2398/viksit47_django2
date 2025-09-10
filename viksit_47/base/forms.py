from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile

class RegisterForm(UserCreationForm):
    full_name = forms.CharField(max_length=255)
    whatsapp_number = forms.CharField(max_length=20)
    gmail = forms.EmailField()
    district_name = forms.CharField(max_length=100)
    taluk_name = forms.CharField(max_length=100)
    college_name = forms.CharField(max_length=255)

    class Meta:
        model = User
        fields = ["username", "password1", "password2", "email"]

    def save(self, commit=True):
        user = super().save(commit)
        Profile.objects.create(
            user=user,
            full_name=self.cleaned_data["full_name"],
            whatsapp_number=self.cleaned_data["whatsapp_number"],
            gmail=self.cleaned_data["gmail"],
            district_name=self.cleaned_data["district_name"],
            taluk_name=self.cleaned_data["taluk_name"],
            college_name=self.cleaned_data["college_name"],
        )
        return user