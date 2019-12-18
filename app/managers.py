from django.db import models
from .models import *

class AllQueryset(models.QuerySet):
    def apteka(self):
        return self.filter(stan__exact = 'A')

    def oddzial(self):
        return self.filter(stan__exact = 'O')


class AllManager(models.Manager):
    def get_queryset(self):
        return AllQueryset(self.model, using=self._db)

    def apteka(self):
        return self.get_queryset().apteka()

    def oddzial(self):
        return self.get_queryset().oddzial()
