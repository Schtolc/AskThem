from django.core.management.base import BaseCommand, CommandError
from myapp.models import Question
from django.contrib.auth.models import User


# import Faker.py


class Command(BaseCommand):
    help = 'Fill the database'

    def handle(self, *args, **options):
        user = User.objects.get(email='nuf@nuf.nu')
        for i in range(1, 10):
            q = Question(author=user, text='text' + str(i), title='title' + str(i))
            q.save()
