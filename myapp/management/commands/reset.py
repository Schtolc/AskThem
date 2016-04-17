from django.core.management.base import BaseCommand, CommandError
from myapp.models import Question, Tag, Answer, Profile
from django.contrib.auth.models import User


class Command(BaseCommand):
    help = 'Reset the database'

    def handle(self, *args, **options):
        Tag.objects.all().delete()
        Question.objects.all().delete()
        Profile.objects.all().delete()
        Answer.objects.all().delete()
