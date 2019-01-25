from django.core.management.base import BaseCommand
from fuzzy_query.smartphone_typo import get_typo_candidates
from django.db.models import Q
from fuzzy_query.models import Word
from timeit import timeit


def do_query(query_str):
    candidate_list = get_typo_candidates(query_str, 200)
    query_filter = Q(Q(name=candidate_list[0]) | Q(name=candidate_list[1]))
    for candidate in candidate_list[2:]:
        query_filter = Q(query_filter | Q(name=candidate))
    result = list(Word.objects.filter(query_filter).all())
    print("Found {} words.".format(len(result)))


class Command(BaseCommand):
    def handle(self, *args, **options):
        print(timeit('do_query("marmorkuchen")', globals=globals(), number=10) / 10)
