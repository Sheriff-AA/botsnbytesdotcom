from .models import Comment, Contact
from django import forms



class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('name',  'body')
        widgets = {
            'name': forms.TextInput(attrs={
                'id': 'name',
                'placeholder': 'Enter your name...', 
                'class': 'w-full mt-1 p-2 border border-gray-300 rounded-lg',
            }),
            'body': forms.Textarea(attrs={
                'id': 'body',
                'placeholder': 'Leave a comment...', 
                'class':"form-control w-full px-0 text-sm text-gray-900 bg-white border-0 dark:bg-gray-800 focus:ring-0 dark:text-white dark:placeholder-gray-400",
                'rows': 4,
                'cols':100,
            }),
        }


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['name', 'email_address', 'message']  # Exclude `date_sent`
        widgets = {
            'name': forms.TextInput(attrs={
                'id': 'name',
                'class': 'w-full mt-1 p-2 border border-gray-300 rounded-lg',
            }),
            'email_address': forms.EmailInput(attrs={
                'id': 'email',
                'class': 'w-full mt-1 p-2 border border-gray-300 rounded-lg',
            }),
            'message': forms.Textarea(attrs={
                'id': 'message',
                'class': 'w-full mt-1 p-2 border border-gray-300 rounded-lg',
                'rows': 4,
            }),
        }

