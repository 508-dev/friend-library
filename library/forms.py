from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from .models import User, Item


class LoginForm(forms.Form):
    """Login form for lenders."""

    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={"autofocus": True}),
    )
    password = forms.CharField(widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request", None)
        self.user = None
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get("username")
        password = cleaned_data.get("password")

        if username and password:
            self.user = authenticate(
                self.request, username=username, password=password
            )
            if self.user is None:
                raise forms.ValidationError("Invalid username or password.")
            if not self.user.is_approved and not self.user.is_superuser:
                raise forms.ValidationError(
                    "Your account is pending approval. Please wait for an admin to approve your registration."
                )
        return cleaned_data


class RegistrationForm(forms.ModelForm):
    """Registration request form."""

    password = forms.CharField(
        widget=forms.PasswordInput,
        help_text="Choose a strong password.",
    )
    password_confirm = forms.CharField(
        widget=forms.PasswordInput,
        label="Confirm password",
    )

    class Meta:
        model = User
        fields = ["username"]

    def clean_password(self):
        password = self.cleaned_data.get("password")
        validate_password(password)
        return password

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")

        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError("Passwords do not match.")
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        user.is_approved = False
        if commit:
            user.save()
        return user


class UserSettingsForm(forms.ModelForm):
    """User settings form for visibility preferences."""

    class Meta:
        model = User
        fields = [
            "show_borrowed_items",
            "show_borrower_name",
            "show_lending_history",
            "show_history_borrower_names",
        ]
        labels = {
            "show_borrowed_items": "Show borrowed items on lending page",
            "show_borrower_name": "Show who is currently borrowing",
            "show_lending_history": "Show lending history on item pages",
            "show_history_borrower_names": "Show borrower names in history",
        }


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
