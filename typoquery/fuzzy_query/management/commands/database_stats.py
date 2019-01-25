from django.core.management.base import BaseCommand
from fuzzy_query.models import Word


class Command(BaseCommand):
    def handle(self, *args, **options):
        print("There are {} words in the database.".format(Word.objects.count()))
