from django import forms
from account.models import *


class ProfileForm(forms.ModelForm):
    class Meta:
        model=UserProfile
        exclude=['user']

class ChangePassword(forms.Form):
    oldpassword=forms.CharField(max_length=100,label="Old Password",widget=forms.PasswordInput(attrs={"class":"form-control","placeholder":"Enter old password"}))
    newpassword=forms.CharField(max_length=100,label="New Password",widget=forms.PasswordInput(attrs={"class":"form-control","placeholder":"Enter new password"}))
    confirmpassword=forms.CharField(max_length=100,label="Confirm Password",widget=forms.PasswordInput(attrs={"class":"form-control","placeholder":"Re-enter the password"}))



class AddBlogForm(forms.ModelForm):
    class Meta:
        model=Blogs
        fields=["title","description","image"]
        widgets={
            "title":forms.TextInput(attrs={"class":"form-control","placeholder":"Enter the title"}),
            "description":forms.Textarea(attrs={"class":"form-control"}),
            "image":forms.FileInput(),
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model=Comments
        fields=["comment"]
        widgets={
            "comment":forms.TextInput(attrs={"class":"form-control","placeholder":"add comment here"}),
        }