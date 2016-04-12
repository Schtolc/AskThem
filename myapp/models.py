from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
import datetime


# Create your models here.


class QuestionManager(models.Manager):
    def new(self):
        self.order_by('-added_at').filter(rating__gt=10)


class Question(models.Model):
    title = models.CharField(max_length=128)
    text = models.TextField()
    added_at = models.DateTimeField(default=datetime.datetime.now)
    author = models.ForeignKey(User)
    rating = models.IntegerField(default=0)
    likes = models.ManyToManyField(User, related_name='voted_user', through='Like')
    objects = QuestionManager()


class Answer(models.Model):
    text = models.TextField()
    author = models.ForeignKey(User)
    question = models.ForeignKey(Question)


class Like(models.Model):
    user = models.ForeignKey(User)
    question = models.ForeignKey(User)
    is_like = models.BooleanField(default=True)
