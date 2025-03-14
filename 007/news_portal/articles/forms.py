from django import forms  
from django.contrib.auth.models import User  
from .models import Article  

class UserRegistrationForm(forms.ModelForm):  
    password = forms.CharField(widget=forms.PasswordInput)  

    class Meta:  
        model = User  
        fields = ['username', 'email', 'password']  


class ArticleForm(forms.ModelForm):  
    class Meta:  
        model = Article  
        fields = ['title', 'content', 'category']