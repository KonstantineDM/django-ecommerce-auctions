from django import forms
from django.forms.widgets import Textarea

from .models import Category, Comment, Listing


class ListingForm(forms.ModelForm):
    title = forms.CharField(max_length=64, label="Title")
    description = forms.CharField(max_length=1024, label="Description", empty_value=True)
    price = forms.DecimalField(max_digits=16, decimal_places=2)
    image = forms.URLField(required=False, empty_value="https://gamepedia.cursecdn.com/ragnarok_gamepedia_en/thumb/1/12/Placeholder_location.png/250px-Placeholder_location.png.jpeg?version=6f64f0c9f146d0ecafb9593b2b1c7a7d")
    category = forms.ModelChoiceField(Category.objects.all(), help_text="Choose a Category")

    class Meta:
        model = Listing
        fields = ("title", "description", "price", "image", "category")


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ("text",)
        widgets = {
            "text": Textarea(attrs={'cols': 100, 'rows': 5, 'default': 'Test comment'}),
        }
