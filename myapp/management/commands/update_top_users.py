from django.core.cache import cache
from myapp.models import *
from django.core.management.base import BaseCommand
import operator


class Command(BaseCommand):
    def handle(self, *args, **options):
        user_rating = {}

        users = User.objects.all()
        for u in users:
            user_rating[str(u.id)] = 0

        questions = Question.objects.all()
        for q in questions:
            user_rating[str(q.author.id)] += 1

        answers = Answer.objects.all()
        for a in answers:
            user_rating[str(a.author.id)] += 1

        # for key in user_rating:
        #     print (unicode(User.objects.get(id=int(key)).username) + ": " + str(user_rating[key]))

        sorted_user_rating = sorted(user_rating.items(), key=operator.itemgetter(1), reverse=True)
        best_users = sorted_user_rating[:10]

        data = [{'name': User.objects.get(id=int(uid[0])).username} for uid in best_users]
        cache.set('best_users', data, 3600)
        print(cache.get('best_users'))
