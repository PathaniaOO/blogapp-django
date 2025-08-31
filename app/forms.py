from django import forms
from app.models import Comments,Subscribe
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comments
        fields = ['content', 'name', 'email', 'website']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['content'].widget.attrs.update({'placeholder': 'Type your comment....'})
        self.fields['name'].widget.attrs.update({'placeholder': 'Name'})
        self.fields['email'].widget.attrs.update({'placeholder': 'Email'})
        self.fields['website'].widget.attrs.update({'placeholder': 'Website'})

class SubscribeForm(forms.ModelForm):
    class Meta:
        model = Subscribe
        fields = '__all__'
        labels = {'email': _(' ')}
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].widget.attrs.update({'placeholder': 'Enter your email to subscribe'})
        
class NewUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'placeholder': 'Username'})
        self.fields['email'].widget.attrs.update({'placeholder': 'Email'})
        self.fields['password1'].widget.attrs.update({'placeholder': 'Create password'})
        self.fields['password2'].widget.attrs.update({'placeholder': 'Confirm password'})
        
    def clean_username(self):
        username = self.cleaned_data.get('username','').lower()
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Username already exists.")
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email','').lower()
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email already exists.")
        return email

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords do not match.")
        return cleaned_data