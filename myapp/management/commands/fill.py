from django.core.management.base import BaseCommand, CommandError
from myapp.models import Question, Tag, Answer
from django.contrib.auth.models import User
from faker import Factory
import random

fake = Factory.create('ru_RU')


class Command(BaseCommand):
    help = 'Fill the database'

    def handle(self, *args, **options):
        # generating tags
        for i in range(0, 10):
            t = Tag(title=fake.word())
            t.save()

        # generating  users
        for i in range(0, 10):
            u = User.objects.create_user(fake.first_name(), email=fake.email(), password=fake.word())
            u.save()

        # generating questions
        for i in range(0, 100):
            user = User.objects.get(id=random.randint(2, 9))
            q = Question(author=user, text=fake.text(), title=fake.street_address(), rating=random.randint(0, 1000))
            q.save()
            random_tag_id = random.randint(2, 9)
            q.tags.add(Tag.objects.get(id=random_tag_id), Tag.objects.get(id=random_tag_id + 1),
                       Tag.objects.get(id=random_tag_id - 1))
            q.save()
            q.likes.add(User.objects.get(id=random_tag_id), User.objects.get(id=random_tag_id + 1),
                        User.objects.get(id=random_tag_id - 1))
            q.save()

        # generating answers
        for i in range(0,1000):
            user = User.objects.get(id=random.randint(1, 10))
            q = Question.objects.get(id=random.randint(1, 100))
            a = Answer(author = user, text = fake.text(), question = q)
            a.save()
