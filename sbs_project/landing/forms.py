from django import forms
from .models import UserInfo

class UserInfoForm(forms.ModelForm):
    class Meta:
        model = UserInfo
        fields = ['first_name', 'last_name', 'phone_number', 'email', 'traveler_class']