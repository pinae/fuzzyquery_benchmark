from django.core.management.base import BaseCommand
from fuzzy_query.models import Word
from random import seed, choice


class Command(BaseCommand):
    def handle(self, *args, **options):
        syllables = ["hun", "kan", "ba", "ni", "so", "wa", "gno", "parr", "lo", "fi", "he", "ta", "to",
                     "ra", "be", "chen", "wun", "mek", "snof", "ail", "toff", "na", "le", "qua", "je",
                     "ol", "ge", "go", "ku", "bröt", "früh", "spät", "mar", "mor", "ap", "fel", "bir"]
        seed(1)

        def gen_word():
            generated_word = ""
            s = choice(syllables)
            while len(generated_word) + len(s) < 255:
                generated_word += s
                if len(generated_word) > 5:
                    if choice([True, False, False]):
                        break
                s = choice(syllables)
            return generated_word

        while Word.objects.count() < 1000000:
            word_name = gen_word()
            if Word.objects.filter(name=word_name).count() > 0:
                word = Word.objects.filter(name=word_name)[0]
                word.count += 1
                word.save()
            else:
                word = Word(name=word_name, count=1)
                word.save()
