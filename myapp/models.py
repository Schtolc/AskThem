from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.http import Http404


# Create your models here.
class AnswerManager(models.Manager):
    def by_id(self, id):
        return self.filter(question=id)

    def new_answer(self, text, author, question):
        a = Answer(text=text, author=author, question=question)
        a.save()
        return self.get(id=a.id)

    def get_page(self, a_id, answers_per_page):
        q = Answer.objects.get(id=a_id).question
        return int(len(Answer.objects.filter(question=q)) / answers_per_page + 1)

    def by_username(self, username):
        u = User.objects.get(username=username)
        return self.filter(author=u)


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

    def new_question(self, title, text, author, tags):
        q = Question(title=title, text=text, author=author)
        q.save()
        for tag in tags.replace(' ', '').split(','):
            t = Tag.objects.all().filter(title=tag).first()
            if not t:
                t = Tag(title=tag)
                t.save()
            q.tags.add(t)
            q.save()
        return self.get(id=q.id)

    def by_username(self, username):
        u = User.objects.get(username=username)
        return self.filter(author=u)


class ProfileManager(models.Manager):
    def new_user(self, username, email, password, pic):
        u = User.objects.create_user(username=username, email=email, password=password)
        u.save()
        p = Profile(avatar=u, picture=pic)
        p.save()

    def change_user(self, new_username, email, old_username):
        u = User.objects.get(username=old_username)
        u.username = new_username
        u.email = email
        u.save()

    def change_password(self, new_password, username):
        u = User.objects.get(username=username)
        u.set_password(new_password)
        u.save()

    def email_in_use(self, email):
        if len(User.objects.all().filter(email=email)) != 0:
            return True
        else:
            return False

    def by_username(self, username):
        u = User.objects.get(username=username)
        return self.get(avatar=u)


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
    picture = models.ImageField()
    objects = ProfileManager()


class Like(models.Model):
    user = models.ForeignKey(User)
    question = models.ForeignKey(Question)
    is_like = models.BooleanField(default=True)
