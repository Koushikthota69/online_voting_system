from django import forms
from django.contrib.auth.models import User
from .models import Vote

class VoteForm(forms.ModelForm):
    college_id = forms.CharField(max_length=20, required=True)

    class Meta:
        model = Vote
        fields = ['candidate', 'college_id']
class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label="Password")
    repassword = forms.CharField(widget=forms.PasswordInput, label="Confirm Password")

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        repassword = cleaned_data.get("repassword")

        if password and repassword and password != repassword:
            raise forms.ValidationError("Passwords do not match!")

        return cleaned_data
