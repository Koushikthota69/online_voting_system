from django import forms
from django.contrib.auth.models import User
from .models import Vote,UserProfile

class VoteForm(forms.ModelForm):
    college_id = forms.CharField(max_length=20, required=True)

    class Meta:
        model = Vote
        fields = ['candidate', 'college_id']

class RegisterForm(forms.ModelForm):
    confirm_password = forms.CharField(widget=forms.PasswordInput, required=True)
    college_id = forms.CharField(max_length=100, required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.set_password(self.cleaned_data["password"])
            user.save()
            # Update the profile created by the signal
            profile = user.userprofile
            profile.college_id = self.cleaned_data["college_id"]
            profile.save()
        return user
class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['college_id']
