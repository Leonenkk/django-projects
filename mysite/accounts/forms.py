from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django import forms


class SignUpForm(UserCreationForm):
    username = forms.CharField(max_length=30)
    email = forms.EmailField(max_length=254)

    class Meta:
        model = get_user_model()# исп. чтобы не привязываться к текущей модели пользователя
        fields = ['username', 'email', 'password1', 'password2']

    def clean_email(self):
        email=self.cleaned_data['email']
        user=get_user_model()
        if user.objects.filter(email=email).exists():
            raise forms.ValidationError(f'Email {email} already registered')
        return email