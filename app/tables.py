import django_tables2 as tables
from .models import Lek

class LekTable(tables.Table):
    class Meta:
        model = Lek
        template_name = "django_tables2/bootstrap.html"
        fields = ("kod_kreskowy",'nazwa','cena_brutto', 'the_count','calosc_brutto' )