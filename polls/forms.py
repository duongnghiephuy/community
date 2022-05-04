from statistics import mode
from attr import fields
from django import forms
from django.forms import ModelForm
from .models import Question
from accounts.models import Community
from django.utils.translation import gettext_lazy as _


class CreateQuestionForm(ModelForm):
    class Meta:
        model = Question
        fields = ["question_text", "community"]
        labels = {
            "question_text": _("Question"),
        }

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["question_text"].widget.attrs.update(
            {
                "placeholder": "Question",
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
