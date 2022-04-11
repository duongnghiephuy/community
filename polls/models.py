from pyexpat import model
from django.db import models
from django.contrib.auth.models import User, Group
from django.contrib.auth.mixins import PermissionRequiredMixin
from rules.contrib.models import RulesModel

# Create your models here.


class Question(RulesModel):

    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField("date publised")
    closed = models.BooleanField(default=False)
    user = models.OneToOneField(User, on_delete=models.SET_NULL)
    group = models.OneToOneField(Group, on_delete=models.CASCADE)

    def get_result_dict(self):
        result = dict()
        for choice in self.choice_set.all():
            result[choice.choice_text] = choice.get_vote_count()
        return result

    def __str__(self):
        return self.question_text


class Choice(RulesModel):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)

    def get_vote_count(self):
        return self.vote_set.count()

    def __str__(self):
        return self.choice_text


class Vote(RulesModel):
    user = models.ForeignKey(User, on_delete=models.SET_NULL)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE)
