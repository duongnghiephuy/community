from pyexpat import model
from statistics import mode
from attr import fields
from django import forms
from django.forms import ModelForm
from idna import alabel
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


class UpdateQuestionStatusForm(forms.Form):
    question = forms.ModelChoiceField(queryset=Question.objects.all(), label="Question")
    closed = forms.BooleanField(required=False, label="Close this question?")

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["question"] = forms.ModelChoiceField(
            queryset=Question.objects.filter(author=user)
        )
