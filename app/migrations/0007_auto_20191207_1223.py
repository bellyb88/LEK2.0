# Generated by Django 3.0 on 2019-12-07 11:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_document'),
    ]

    operations = [
        migrations.AlterField(
            model_name='faktura',
            name='wartosc_brutto',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='faktura',
            name='wartosc_netto',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='lek',
            name='cena_brutto',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='lek',
            name='cena_netto',
            field=models.FloatField(blank=True, null=True),
        ),
    ]