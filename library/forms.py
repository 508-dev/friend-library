from django import forms
from .models import Item


class ItemForm(forms.ModelForm):
    """Form for creating/editing items."""

    class Meta:
        model = Item
        fields = [
            "title",
            "short_description",
            "long_description",
            "image",
            "borrow_time_limit",
        ]
        widgets = {
            "short_description": forms.Textarea(attrs={"rows": 2}),
            "long_description": forms.Textarea(attrs={"rows": 5}),
        }
