from django import forms

from logic.models import Person


class UserForm(forms.ModelForm):
    name=forms.CharField(label='Имя',help_text='Введите свое имя', min_length=2, max_length=10)
    age=forms.IntegerField(label='Возраст',label_suffix='',help_text='Введите ваш возраст',min_value=1,max_value=100)

    class Meta:
        model = Person
        fields=['name','age']