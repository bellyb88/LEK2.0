from django.db import models
from .managers import *
# Create your models here.
class Document(models.Model):
    document = models.FileField(upload_to='documents/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

class Faktura(models.Model):
    nr_faktury = models.BigIntegerField(null=True, blank=True)
    data_wystawienia = models.DateField(null=True, blank=True)
    data_sprzedazy = models.DateField(null=True, blank=True)
    termin_platnosci = models.DateField(null=True, blank=True)
    id_sprzedawcy = models.PositiveIntegerField(null=True, blank=True)
    korekta = models.BooleanField()
    wartosc_netto = models.FloatField(null=True, blank=True)
    wartosc_brutto = models.FloatField(null=True, blank=True)

    def __str__(self):
        return str(self.nr_faktury)

    class Meta:
        verbose_name_plural = "Faktury"



class Lek(models.Model):
    id_towaru = models.PositiveIntegerField(null=True, blank=True)
    nazwa = models.CharField(max_length=300, blank=True)
    BLOZ = models.PositiveIntegerField(null=True, blank=True)
    jednostka = models.CharField(max_length=10, blank=True)
    seria = models.CharField(max_length=50, blank=True)
    data_waznosci = models.DateField(null=True, blank=True)
    cena_netto = models.FloatField(null=True, blank=True)
    cena_brutto = models.FloatField(null=True, blank=True)
    PKWiU =  models.CharField(max_length=50, blank=True)
    kod_kreskowy = models.BigIntegerField(null=True, blank=True)
    faktura = models.ForeignKey(Faktura, on_delete=models.CASCADE, null=True, blank=True)
    stan = models.CharField(max_length=3,blank=True, choices=(('A','A'),('O', 'O') ))

    all = AllManager()
    def __str__(self):
        return self.nazwa

    class Meta:
        verbose_name_plural = "Leki"
