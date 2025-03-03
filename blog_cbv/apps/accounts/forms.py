from django import forms
from django.contrib.auth.models import User

from apps.accounts.models import Profile


class UserUpdateForm(forms.ModelForm):
    username = forms.CharField(max_length=100,widget=forms.TextInput(attrs={'class': 'form-control mb-1'}))
    email = forms.EmailField(widget=forms.TextInput(attrs={'class': 'form-control mb-1'}))
    first_name=forms.CharField(max_length=100,widget=forms.TextInput(attrs={'class': 'form-control mb-1'}))
    last_name=forms.CharField(max_length=100,widget=forms.TextInput(attrs={'class': 'form-control mb-1'}))

    class Meta:
       model = User
       fields = ('username','email','first_name','last_name')

    def clean_email(self):
        email=self.cleaned_data.get('email')
        if email and User.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError('Email адрес должен быть уникальным')
        return email


class ProfileUpdateForm(forms.ModelForm):
    slug = forms.SlugField(widget=forms.TextInput(attrs={'class': 'form-control mb-1'}))
    birth_date=forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control mb-1'}))
    bio=forms.CharField(widget=forms.Textarea(attrs={'rows': 5, 'class': 'form-control mb-1'}))
    avatar=forms.ImageField(widget=forms.FileInput(attrs={'class': 'form-control mb-1'}))

    class Meta:
        model=Profile
        fields=('slug','bio','birth_date','avatar')