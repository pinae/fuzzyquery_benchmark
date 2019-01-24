from django.db import models


class Word(models.Model):
    name = models.CharField(max_length=256)
    count = models.IntegerField(default=1)
