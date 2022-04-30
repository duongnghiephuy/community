from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import Community
from django.forms import ModelForm
from django import forms


# Subclass form to add class for CSS style
class CustomLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].widget.attrs.update(
            {"class": "my-username-class", "placeholder": "username"}
        )
        self.fields["password"].widget.attrs.update(
            {"class": "my-password-class", "placeholder": "password"}
        )


class CommunityCreationForm(ModelForm):

    address = forms.CharField(
        max_length=600, widget=forms.TextInput(attrs={"placeholder": "Address"})
    )

    class Meta:
        model = Community
        fields = ["name", "description", "image"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["name"].widget.attrs.update({"placeholder": "Name"})
        self.fields["description"].widget.attrs.update({"placeholder": "Description"})

        for visible in self.visible_fields():
            visible.field.widget.attrs.update(
                {
                    "class": "form-control",
                }
            )
