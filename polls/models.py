from pyexpat import model
from django.db import models
from django.contrib.auth.models import User, Group

# Create your models here.


class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField("date publised")
    closed = models.BooleanField(default=False)
    author = models.OneToOneField(User, on_delete=models.SET_NULL)
    community = models.OneToOneField(Group, on_delete=models.CASCADE)

    def __str__(self):
        return self.question_text


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text
