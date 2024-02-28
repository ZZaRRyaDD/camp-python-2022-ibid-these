
from django.contrib.auth.forms import UserCreationForm
from django.forms import Textarea, TextInput
from django.forms.models import ModelForm

from . import models


class RegistrationForm(UserCreationForm):
    """Form for user registration."""

    class Meta:
        model = models.User
        fields = [
            "email",
            "password1",
            "password2",
            "first_name",
            "last_name",
            "avatar",
            "birthday",
            "contact_info",
        ]
        widgets = {
            "contact_info": Textarea(attrs={"cols": 60, "rows": 4}),
            "birthday": TextInput(attrs={"type": "date"}),
        }


class UserEditForm(ModelForm):
    """Form for editing user information."""

    class Meta:
        model = models.User
        fields = [
            "first_name",
            "last_name",
            "avatar",
            "birthday",
            "contact_info",
        ]
        widgets = {
            "contact_info": Textarea(attrs={"cols": 60, "rows": 4}),
            "birthday": TextInput(attrs={"type": "date"}),
        }
