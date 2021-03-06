from allauth.account.forms import SignupForm
from django import forms

from .models import Category, Photo, Profile


class PhotoForm(forms.ModelForm):
    category = forms.ModelChoiceField(
        required=False, queryset=Category.objects.all(), )

    class Meta:
        model = Photo
        fields = [
            'image',
            'description'
        ]


class ProfileForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = [
            'card_image',
            'avatar',
            'bio',
        ]


class CustomSignupForm(SignupForm):
    first_name = forms.CharField(max_length=30, label='First Name')
    last_name = forms.CharField(max_length=30, label='Last Name')

    def signup(self, request, user):
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.save()

        return user


class UserLoginForm(forms.Form):
    username = forms.CharField(label='Email')
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
