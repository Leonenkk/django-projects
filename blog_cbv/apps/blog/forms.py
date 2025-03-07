from django import forms
from django_ckeditor_5.widgets import CKEditor5Widget
from apps.blog.models import Post, Comment


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'description', 'text', 'trumbnail', 'status', 'category']

    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': 'form-control',
                'autocomplete': 'off'
            })
        self.fields['description'].widget = CKEditor5Widget(config_name='awesome_editor')
        self.fields['text'].widget = CKEditor5Widget(config_name='awesome_editor')


class PostUpdateForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = PostForm.Meta.fields + ['fixed']

    def __init__(self, *args, **kwargs):
        super(PostUpdateForm, self).__init__(*args, **kwargs)
        self.fields['fixed'].widget.attrs.update({
            'class': 'form-check-input'
        })


class CommentForm(forms.ModelForm):
    parent = forms.IntegerField(widget=forms.HiddenInput, required=False)
    content = forms.CharField(label='', widget=forms.Textarea(
        attrs={'cols': 30, 'rows': 5, 'placeholder': 'Комментарий', 'class': 'form-control'}))

    class Meta:
        model = Comment
        fields = ['content']
