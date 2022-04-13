from django.db import models
from django.contrib.auth.models import User, Group


# Create your models here.


class Question(models.Model):

    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField("date publised")
    closed = models.BooleanField(default=False)
    author = models.ForeignKey(User, on_delete=models.SET_NULL)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)

    def get_result_dict(self):
        result = dict()
        for choice in self.choice_set.all():
            result[choice.choice_text] = choice.get_vote_count()
        return result

    def __str__(self):
        return self.question_text

    def is_author(self, user):
        if user == self.author:
            return True
        return False

    def is_voter(self, user):
        if self.is_author() or user.groups.filter(name=self.group).exists():
            return True
        return False


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)

    def get_vote_count(self):
        return self.vote_set.count()

    def __str__(self):
        return self.choice_text


class Vote(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE)
