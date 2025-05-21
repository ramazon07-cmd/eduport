from django import forms
from .models import Contact, Comment

class CreateContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['name', 'email', 'message']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': "form-control form-control-lg bg-light-input",
                'id': 'yourName'
            }),
            'email': forms.EmailInput(attrs={
                'class': "form-control form-control-lg bg-light-input",
                'id': 'emailInput'
            }),
            'message': forms.Textarea(attrs={
                'class': "form-control bg-light-input",
                'id': 'textareaBox',
                'rows': 4
            }),
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['body']
        widgets = {
            'body': forms.Textarea(attrs={
                'class': 'one form-control pe-4 bg-light',
                'id': 'autoheighttextarea',
                'rows': 1,
                'placeholder': 'Add a comment...'
            }),
        }

    def save(self, commit=True):
        comment = super().save(commit=False)

        if commit:
            comment.save()

        return comment
