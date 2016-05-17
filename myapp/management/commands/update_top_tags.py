from django.core.cache import cache
from myapp.models import *
from django.core.management.base import BaseCommand
import operator


class Command(BaseCommand):
    def handle(self, *args, **options):
        tags_rating = {}

        tags = Tag.objects.all()
        for t in tags:
            tags_rating[t.title] = 0

        questions = Question.objects.all()
        for q in questions:
            for tag in q.tags.all():
                tags_rating[tag.title] += 1

        sorted_tags_rating = sorted(tags_rating.items(), key=operator.itemgetter(1), reverse=True)
        best_users = sorted_tags_rating[:10]

        data = [{'name': tag[0]} for tag in best_users]
        cache.set('best_tags', data, 3600)
        print(cache.get('best_tags'))
