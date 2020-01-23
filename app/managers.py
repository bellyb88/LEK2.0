from django.db import models
from .models import *

class AllQueryset(models.QuerySet):
    def apteka(self):
        return self.filter(stan__exact = 'A')

    def oddzial(self):
        return self.filter(stan__exact = 'O')

    def psychotrop(self):
        list =['05909990166411', '05909990135516','05909990135615','05909990093717','05909990093724',
        '05909990149513', '05909990149612','05909991271374','5909990966127', '5909990966226']
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
