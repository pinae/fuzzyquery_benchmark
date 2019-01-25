from django.core.management.base import BaseCommand
from django.db.models import Q
from fuzzy_query.models import Word
from fuzzy_query.smartphone_typo import levensteinish_probability
from timeit import timeit


def do_query(query_str):
    pair_list = []
    for i in range(len(query_str) - 1):
        if query_str[i:i+2] not in pair_list:
            pair_list.append(query_str[i:i + 2])
    or_filter = Q()
    for p_o in pair_list:
        query_filter = Q()
        for p_i in pair_list:
            if p_o != p_i:
                query_filter = Q(query_filter & Q(name__icontains=p_i))
        or_filter = Q(or_filter | query_filter)
    result = []
    for word in Word.objects.filter(or_filter).all():
        result.append((levensteinish_probability(word.name, query_str), word.name))
    print("Found {} words.".format(len(result)))
    for ri in sorted(result, reverse=True):
        print(" p={} - {}".format(*ri))


class Command(BaseCommand):
    def handle(self, *args, **options):
        print(timeit('do_query("marmorkuchen")', globals=globals(), number=10) / 10)
