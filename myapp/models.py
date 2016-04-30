from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.http import Http404


# Create your models here.
class AnswerManager(models.Manager):
    def by_id(self, id):
        return self.filter(question=id)


class QuestionManager(models.Manager):
    def new(self):
        return self.order_by('-added_at')

    def hot(self):
        return self.order_by('-rating')

    def by_tags(self, tag):
        return self.filter(tags__title=tag)

    def by_id(self, q_id):
        try:
            return self.get(id=q_id)
        except Question.DoesNotExist:
            raise Http404("Question does not exist")


class Tag(models.Model):
    title = models.CharField(max_length=128, unique=True)


class Question(models.Model):
    title = models.CharField(max_length=128)
    text = models.TextField()
    added_at = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User)
    rating = models.IntegerField(default=0)
    tags = models.ManyToManyField(Tag)
    likes = models.ManyToManyField(User, related_name='likes_users', through='Like')
    objects = QuestionManager()


class Answer(models.Model):
    text = models.TextField()
    author = models.ForeignKey(User)
    question = models.ForeignKey(Question)
    added_at = models.DateTimeField(default=timezone.now)
    objects = AnswerManager()


class Profile(models.Model):
    avatar = models.OneToOneField(User)
    pic = models.CharField(max_length=128)

class Like(models.Model):
    user = models.ForeignKey(User)
    question = models.ForeignKey(Question)
    is_like = models.BooleanField(default=True)