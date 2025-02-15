from django import forms

from blog.models import Comment


class EmailForm(forms.Form):
    email=forms.EmailField()
    name=forms.CharField(max_length=50)
    to=forms.EmailField()
    comments=forms.CharField(widget=forms.Textarea,required=False)

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields=('name','email','body')


class SearchForm(forms.Form):
    query=forms.CharField()