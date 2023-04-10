from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import password_validation


class Regform(UserCreationForm):
    error_messages = {
        "password_mismatch":("The two password fields didn’t match."),
    }
    password1 = forms.CharField(
        label=("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password",'class':'form-control','placeholder':'Enter your Password'}),
        help_text=password_validation.password_validators_help_text_html(),
    )
    password2 = forms.CharField(
        label=("Password confirmation"),
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password",'class':'form-control','placeholder':'Repeat your Password'}),
        strip=False,
        help_text=("Enter the same password as before, for verification."),
    )
    class Meta:
        model=User
        fields=['first_name','last_name','email','username','password1','password2']
        widgets={
            "first_name":forms.TextInput(attrs={"class":"form-control","placeholder":"Enter First Name"}),
            "last_name":forms.TextInput(attrs={"class":"form-control","placeholder":"Enter Last Name"}),
            "email":forms.EmailInput(attrs={"class":"form-control","placeholder":"Enter Email"}),
            "username":forms.TextInput(attrs={"class":"form-control","placeholder":"Enter Username"}),
            "password1":forms.PasswordInput(attrs={"class":"form-control","placeholder":"Enter Password"}),
            "password2":forms.PasswordInput(attrs={"class":"form-control","placeholder":"Confirm Password"}),
        }

class Logform(forms.Form):
    username=forms.CharField(max_length=100,widget=forms.TextInput(attrs={"class":"form-control","placeholder":"Enter Username"}))
    password=forms.CharField(max_length=100,widget=forms.PasswordInput(attrs={"class":"form-control","placeholder":"Enter Password"}))
