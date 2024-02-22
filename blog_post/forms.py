from .models import *
from django import forms


class BlogPostForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = ("title", "content", "image")
        widgets = {
            "title": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Title of the Blog"}
            ),
            "content": forms.Textarea(
                attrs={"class": "form-control", "placeholder": "Content of the Blog"}
            ),
        }


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = (
            "phone_no",
            "bio",
            "facebook",
            "instagram",
            "linkedin",
            "image",
        )
