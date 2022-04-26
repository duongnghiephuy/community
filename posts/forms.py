from django import forms
from django.forms import ModelForm
from .models import Post
from django.contrib.auth.models import User, Group
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
            "group",
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
        self.fields["group"] = forms.ModelChoiceField(
            user.groups.all(), empty_label="Group"
        )
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

        for visible in self.visible_fields():
            visible.field.widget.attrs.update(
                {
                    "class": "form-control",
                }
            )
