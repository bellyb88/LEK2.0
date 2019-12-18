# Generated by Django 3.0 on 2019-12-07 10:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_lek_faktura'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='faktura',
            options={'verbose_name_plural': 'Faktury'},
        ),
        migrations.AlterModelOptions(
            name='lek',
            options={'verbose_name_plural': 'Leki'},
        ),
        migrations.RenameField(
            model_name='lek',
            old_name='BOLZ',
            new_name='BLOZ',
        ),
        migrations.AddField(
            model_name='lek',
            name='stan',
            field=models.CharField(blank=True, choices=[('A', 'A'), ('O', 'O')], max_length=3),
        ),
    ]
