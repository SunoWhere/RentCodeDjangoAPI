# Generated by Django 5.1.4 on 2024-12-13 21:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rentcode', '0001_initial'),
        ('sales', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='codes',
            field=models.ManyToManyField(related_name='clients', to='rentcode.code'),
        ),
    ]
