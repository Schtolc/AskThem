from django.core.management.base import BaseCommand, CommandError
from myapp.models import Question, Tag, Answer, Profile
from django.contrib.auth.models import User
from django.db import connection


class Command(BaseCommand):
    help = 'Reset the database'

    def handle(self, *args, **options):
        Tag.objects.all().delete()
        Question.objects.all().delete()
        Profile.objects.all().delete()
        Answer.objects.all().delete()
        User.objects.all().delete()

        cursor = connection.cursor()
        cursor.execute('ALTER TABLE  myapp_tag AUTO_INCREMENT=0')
        cursor.execute('ALTER TABLE  myapp_answer AUTO_INCREMENT=0')
        cursor.execute('ALTER TABLE  myapp_profile AUTO_INCREMENT=0')
        cursor.execute('ALTER TABLE  myapp_question AUTO_INCREMENT=0')
        cursor.execute('ALTER TABLE  myapp_like AUTO_INCREMENT=0')
        cursor.execute('ALTER TABLE  myapp_question_tags AUTO_INCREMENT=0')
        cursor.execute('ALTER TABLE  auth_user AUTO_INCREMENT=0')

