from django.db import models
from django.contrib.auth.models import User
from datetime import date, time
import math

# Create your models here.

class Topic(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=200)
    text = models.TextField()

    def __str__(self):
        return self.name


class Favourite(models.Model):
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.user) + ' favourited ' + str(self.topic)


class TextQuestion(models.Model):
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    question = models.CharField(max_length=200)
    answer = models.CharField(max_length=200)

    def __str__(self):
        return str(self.topic) + " exam question"


class MultipleChoiceQuestion(models.Model):
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    question = models.CharField(max_length=200)
    op1 = models.CharField(max_length=200,null=True)
    op2 = models.CharField(max_length=200,null=True)
    op3 = models.CharField(max_length=200,null=True)
    op4 = models.CharField(max_length=200,null=True)
    ans = models.CharField(max_length=200,null=True)

    def __str__(self):
        return str(self.topic) + " exam question"


class TrueFalseQuestion(models.Model):
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    question = models.CharField(max_length=200)
    answer = models.BooleanField()

    def __str__(self):
        return str(self.topic) + " exam question"

class ExamResult(models.Model):
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.CharField(max_length=10)
    date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.user.username) + "'s scored " + str(self.score) + " on the " + str(self.topic) + " exam on " + str(self.date.date()) + " at " + str(self.date.time().replace(microsecond=0))

    def passed(self):
        return int(str(self.score).split('/')[0]) >= math.floor(0.7 * int(str(self.score).split('/')[1]))

