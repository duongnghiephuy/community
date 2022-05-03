from django import forms
from django.forms import ModelForm
from .models import Post
from django.contrib.auth.models import User
from accounts.models import Community
from django.utils.translation import gettext_lazy as _


class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = [
            "post_title",
            "post_content",
            "post_image",
            "schedule_from",
            "schedule_to",
            "community",
        ]
        widgets = {
            "schedule_from": forms.DateTimeInput(attrs={"type": "datetime-local"}),
            "schedule_to": forms.DateTimeInput(attrs={"type": "datetime-local"}),
        }
        labels = {
            "post_title": _("Title"),
            "post_content": _("Content"),
            "post_image": _("Item image"),
        }

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["post_content"].widget.attrs.update(
            {
                "placeholder": "Content",
            }
        )
        self.fields["post_title"].widget.attrs.update(
            {
                "placeholder": "Title",
            }
        )

        self.fields["community"] = forms.ModelChoiceField(
            queryset=Community.objects.filter(users=user)
        )

        for visible in self.visible_fields():
            visible.field.widget.attrs.update(
                {
                    "class": "form-control",
                }
            )
