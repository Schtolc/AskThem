from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


# Create your models here.
class AnswerManager(models.Manager):
    @staticmethod
    def by_id(id):
        return Answer.objects.filter(question=id)


class QuestionManager(models.Manager):
    @staticmethod
    def new():
        return Question.objects.order_by('-added_at')

    @staticmethod
    def hot():
        return Question.objects.order_by('-rating')

    @staticmethod
    def by_tags(tag):
        return Question.objects.filter(tags__title=tag)

    @staticmethod
    def by_id(q_id):
        return Question.objects.get(id=q_id)


class Tag(models.Model):
    title = models.CharField(max_length=128)


class Question(models.Model):
    title = models.CharField(max_length=128)
    text = models.TextField()
    added_at = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User)
    rating = models.IntegerField(default=0)
    tags = models.ManyToManyField(Tag)
    likes = models.ManyToManyField(User, related_name='likes_users')
    manager = QuestionManager


class Answer(models.Model):
    text = models.TextField()
    author = models.ForeignKey(User)
    question = models.ForeignKey(Question)
    added_at = models.DateTimeField(default=timezone.now)
    manager = AnswerManager


class Profile(models.Model):
    avatar = models.OneToOneField(User)
    pic = models.CharField(max_length=128)
