# Generated by Django 3.0.1 on 2020-01-11 15:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0009_auto_20191219_2043'),
    ]

    operations = [
        migrations.AddField(
            model_name='lek',
            name='data_wydania',
            field=models.DateField(blank=True, null=True),
        ),
    ]
