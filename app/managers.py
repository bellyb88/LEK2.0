from django.db import models
from .models import *

class AllQueryset(models.QuerySet):
    def apteka(self):
        return self.filter(stan__exact = 'A')

    def oddzial(self):
        return self.filter(stan__exact = 'O')

    def psychotrop(self):
        list =[]
        return self.filter(kod_kreskowy__in = list)

class AllManager(models.Manager):
    def get_queryset(self):
        return AllQueryset(self.model, using=self._db)

    def apteka(self):
        return self.get_queryset().apteka()

    def oddzial(self):
        return self.get_queryset().oddzial()

    def psychotrop(self):
        return self.get_queryset().psychotrop()
