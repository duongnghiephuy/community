from django.contrib.auth.forms import AuthenticationForm
from .models import Community
from django.forms import ModelForm


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
    class Meta:
        model = Community
        fields = ["name", "description", "location", "image"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["name"].widget.attrs.update({"placeholder": "Name"})
        self.fields["description"].widget.attrs.update({"placeholder": "Description"})
        self.fields["location"].widget.attrs.update({"placeholder": "Location"})

        for visible in self.visible_fields():
            visible.field.widget.attrs.update(
                {
                    "class": "form-control",
                }
            )
