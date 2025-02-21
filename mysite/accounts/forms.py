from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms

from accounts.models import Profile


class SingUpForm(UserCreationForm):
    username = forms.CharField(min_length=3, max_length=64)
    email = forms.EmailField(max_length=254)
    first_name = forms.CharField(max_length=64)
    last_name = forms.CharField(max_length=64)
    password1 = forms.CharField(min_length=8, max_length=64, widget=forms.PasswordInput)
    password2 = forms.CharField(min_length=8, max_length=64, widget=forms.PasswordInput)

    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data['email']
        user = get_user_model()
        if user.objects.filter(email=email).exists():
            raise forms.ValidationError(f'Email {email} already registered')
        return email


class LoginForm(AuthenticationForm):
    username = forms.CharField(max_length=100,
                               required=True,
                               widget=forms.TextInput(attrs={'placeholder': 'Username'}))
    password = forms.CharField(max_length=50,
                               required=True,
                               widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))
    remember_me = forms.BooleanField(required=False)

    class Meta:
        model = get_user_model()
        fields = ['username', 'password', 'remember_me']



class UserUpdateForm(forms.ModelForm):
    username = forms.CharField(min_length=3,
                               max_length=64,
                               required=True,
                               widget=forms.TextInput())
    email=forms.EmailField(max_length=254,
                           required=True,
                           widget=forms.TextInput())

    class Meta:
        model = get_user_model()
        fields = ['username', 'email']


class ProfileUpdateForm(forms.ModelForm):
    avatar=forms.ImageField(widget=forms.FileInput())
    biography=forms.CharField(widget=forms.Textarea())

    class Meta:
        model=Profile
        fields=['avatar','biography']